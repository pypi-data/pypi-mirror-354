from __future__ import annotations

import typing

from fuzzy_dl_owl2.fuzzydl.classification_node import ClassificationNode
from fuzzy_dl_owl2.fuzzydl.concept.concept import Concept
from fuzzy_dl_owl2.fuzzydl.concept.implies_concept import ImpliesConcept
from fuzzy_dl_owl2.fuzzydl.concept.operator_concept import OperatorConcept
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
from fuzzy_dl_owl2.fuzzydl.query.subsumption_query import SubsumptionQuery
from fuzzy_dl_owl2.fuzzydl.util.config_reader import ConfigReader
from fuzzy_dl_owl2.fuzzydl.util.constants import LogicOperatorType, VariableType


class MinSubsumesQuery(SubsumptionQuery):
    """
    Minimize subsumption query.
    """

    def __init__(self, c1: Concept, c2: Concept, type_: LogicOperatorType) -> None:
        super().__init__(c1, c2, type_)

    def preprocess(self, kb: KnowledgeBase) -> None:
        if kb.is_classified():
            return

        ind: Individual = kb.get_new_individual()

        if self.type == LogicOperatorType.LUKASIEWICZ:
            conc: Concept = OperatorConcept.lukasiewicz_or(-self.c2, self.c1)
        elif self.type == LogicOperatorType.GOEDEL:
            conc: Concept = ImpliesConcept.goedel_implies(self.c2, self.c1)
        elif self.type == LogicOperatorType.ZADEH:
            conc: Concept = ImpliesConcept.zadeh_implies(self.c2, self.c1)
        else:  # LogicOperatorType.KLEENE_DIENES
            conc: Concept = OperatorConcept.goedel_or(-self.c2, self.c1)

        q: Variable = kb.milp.get_new_variable(VariableType.SEMI_CONTINUOUS)
        kb.old_01_variables += 1
        self.obj_expr: Expression = Expression(Term(1.0, q))

        # a: not c or d >= 1-q
        kb.add_assertion(
            ind,
            -conc,
            DegreeExpression.get_degree(Expression(1.0, Term(-1.0, q))),
        )
        kb.solve_assertions()

    # def solve(self, kb: KnowledgeBase) -> Solution:
    #     try:
    #         self.set_initial_time()
    #         if ConfigReader.OPTIMIZATIONS == 0 or kb.has_nominals_in_tbox():
    #             cloned: KnowledgeBase = kb.clone()
    #             cloned.solve_abox()
    #         else:
    #             cloned: KnowledgeBase = kb.clone_without_abox()
    #         self.preprocess(cloned)
    #         sol: Solution = cloned.optimize(self.obj_expr)
    #         self.set_total_time()
    #         return sol
    #     except InconsistentOntologyException:
    #         return Solution(Solution.INCONSISTENT_KB)

    def solve(self, kb: KnowledgeBase) -> Solution:
        try:
            self.set_initial_time()
            if kb.is_classified() and self.c1.is_atomic() and self.c2.is_atomic():
                n1: typing.Optional[ClassificationNode] = kb.get_classification_node(
                    str(self.c1)
                )
                n2: typing.Optional[ClassificationNode] = kb.get_classification_node(
                    str(self.c2)
                )
                if n1 is not None and n1.is_thing():
                    sol: Solution = Solution(1.0)
                elif n2 is not None and n1.is_thing():
                    sol: Solution = Solution(1.0)
                else:
                    sol: Solution = Solution(kb.get_subsumption_flags(n1, n2))
            else:
                if ConfigReader.OPTIMIZATIONS == 0 or kb.has_nominals_in_tbox():
                    cloned: KnowledgeBase = kb.clone()
                    cloned.solve_abox()
                else:
                    cloned: KnowledgeBase = kb.clone_without_abox()
                self.preprocess(cloned)
                sol: Solution = cloned.optimize(self.obj_expr)

            self.set_total_time()
            return sol
        except InconsistentOntologyException:
            return Solution(Solution.INCONSISTENT_KB)

    def __str__(self) -> str:
        return f"{self.c1} subsumes {self.c2} ? >= "
