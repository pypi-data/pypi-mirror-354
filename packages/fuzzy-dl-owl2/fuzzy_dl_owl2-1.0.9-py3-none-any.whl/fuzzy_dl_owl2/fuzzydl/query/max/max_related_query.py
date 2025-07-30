from __future__ import annotations

from fuzzy_dl_owl2.fuzzydl.concept.concept import Concept
from fuzzy_dl_owl2.fuzzydl.concept.has_value_concept import HasValueConcept
from fuzzy_dl_owl2.fuzzydl.degree.degree_variable import DegreeVariable
from fuzzy_dl_owl2.fuzzydl.exception.inconsistent_ontology_exception import (
    InconsistentOntologyException,
)
from fuzzy_dl_owl2.fuzzydl.individual.individual import Individual
from fuzzy_dl_owl2.fuzzydl.knowledge_base import KnowledgeBase
from fuzzy_dl_owl2.fuzzydl.milp.expression import Expression
from fuzzy_dl_owl2.fuzzydl.milp.solution import Solution
from fuzzy_dl_owl2.fuzzydl.milp.term import Term
from fuzzy_dl_owl2.fuzzydl.milp.variable import Variable
from fuzzy_dl_owl2.fuzzydl.query.related_query import RelatedQuery


class MaxRelatedQuery(RelatedQuery):
    """
    Lowest upper bound of a role assertion (ind1, ind2, role)
    """

    def __init__(self, a: Individual, b: Individual, role_name: str) -> None:
        self.ind1: Individual = a
        self.ind2: Individual = b
        self.role: str = role_name

    def preprocess(self, kb: KnowledgeBase) -> None:
        # glb(ind1 : b-some R ind2)
        conc: Concept = HasValueConcept(self.role, self.ind2)
        q: Variable = kb.milp.get_variable(self.ind1, conc)
        kb.add_assertion(self.ind1, conc, DegreeVariable.get_degree(q))
        kb.old_01_variables += 1
        self.obj_expr: Expression = Expression(Term(-1.0, q))
        kb.solve_assertions()

    def solve(self, kb: KnowledgeBase) -> Solution:
        try:
            self.set_initial_time()
            kb.solve_abox()
            cloned: KnowledgeBase = kb.clone()
            self.preprocess(cloned)
            sol: Solution = cloned.optimize(self.obj_expr)
            self.set_total_time()
            return sol
        except InconsistentOntologyException:
            return Solution(Solution.INCONSISTENT_KB)

    def __str__(self) -> str:
        return f"Is {self.ind1} related to {self.ind2} through {self.role} ? <= "
