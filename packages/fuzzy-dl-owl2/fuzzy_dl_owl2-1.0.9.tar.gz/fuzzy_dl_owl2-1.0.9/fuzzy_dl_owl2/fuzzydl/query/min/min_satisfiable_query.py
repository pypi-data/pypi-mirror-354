from __future__ import annotations

import typing

from fuzzy_dl_owl2.fuzzydl.concept.concept import Concept
from fuzzy_dl_owl2.fuzzydl.degree.degree_expression import DegreeExpression
from fuzzy_dl_owl2.fuzzydl.exception.inconsistent_ontology_exception import (
    InconsistentOntologyException,
)
from fuzzy_dl_owl2.fuzzydl.individual.individual import Individual
from fuzzy_dl_owl2.fuzzydl.knowledge_base import KnowledgeBase
from fuzzy_dl_owl2.fuzzydl.milp.expression import Expression
from fuzzy_dl_owl2.fuzzydl.milp.solution import Solution
from fuzzy_dl_owl2.fuzzydl.milp.term import Term
from fuzzy_dl_owl2.fuzzydl.milp.variable import Variable
from fuzzy_dl_owl2.fuzzydl.query.satisfiable_query import SatisfiableQuery
from fuzzy_dl_owl2.fuzzydl.util.config_reader import ConfigReader
from fuzzy_dl_owl2.fuzzydl.util.constants import VariableType


class MinSatisfiableQuery(SatisfiableQuery):
    """
    Minimal satisfiability degree of a fuzzy concept.
    """

    @typing.overload
    def __init__(self, c: Concept) -> None: ...

    @typing.overload
    def __init__(self, c: Concept, a: Individual) -> None: ...

    def __init__(self, *args) -> None:
        assert len(args) in [1, 2]
        assert isinstance(args[0], Concept)
        if len(args) == 1:
            self.__min_sat_query_init_1(*args)
        else:
            assert isinstance(args[1], Individual)
            self.__min_sat_query_init_2(*args)

    def __min_sat_query_init_1(self, c: Concept) -> None:
        """
        Constructor for a general satisfiability query.

        Args:
            c (Concept): A fuzzy concept for which the satisfiability is to be tested.
        """
        super().__init__(c)

    def __min_sat_query_init_2(self, c: Concept, a: Individual) -> None:
        """
        Constructor for a satisfiability query involving a specific individual.

        Args:
            c (Concept): A fuzzy concept for which the satisfiability is to be tested.
            a (Individual): An individual used in the satisfiability test.
        """
        super().__init__(c, a)

    def preprocess(self, kb: KnowledgeBase) -> None:
        if "(some " in str(self.conc) or "(b-some " in str(self.conc):
            kb.set_dynamic_blocking()
        q: Variable = kb.milp.get_new_variable(VariableType.SEMI_CONTINUOUS)
        kb.old_01_variables += 1
        self.obj_expr: Expression = Expression(Term(1.0, q))
        kb.add_assertion(
            self.ind,
            -self.conc,
            DegreeExpression.get_degree(Expression(1.0, Term(-1.0, q))),
        )
        kb.solve_assertions()

    def solve(self, kb: KnowledgeBase) -> Solution:
        try:
            self.set_initial_time()
            kb.old_binary_variables += 1
            use_abox = self.ind is not None or ConfigReader.OPTIMIZATIONS == 0
            cloned: KnowledgeBase = kb.clone() if use_abox else kb.clone_without_abox()
            if self.ind is None:
                self.ind: Individual = cloned.get_new_individual()
            if use_abox:
                cloned.solve_abox()
            self.preprocess(cloned)
            sol: Solution = cloned.optimize(self.obj_expr)
            if sol.get_solution() < 0.0:
                sol = Solution(-sol.get_solution())
            self.set_total_time()
            return sol

        except InconsistentOntologyException:
            return Solution(Solution.INCONSISTENT_KB)

    def __str__(self) -> str:
        if self.ind is not None:
            return f"Is Concept {self.conc} satisfiable? [Individual {self.ind}] >= "
        return f"Is Concept {self.conc} satisfiable? >= "
