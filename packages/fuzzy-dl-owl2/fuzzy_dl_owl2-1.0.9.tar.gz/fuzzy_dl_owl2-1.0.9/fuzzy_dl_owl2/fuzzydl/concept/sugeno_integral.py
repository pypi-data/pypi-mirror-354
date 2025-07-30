from __future__ import annotations

import typing

import trycast

from fuzzy_dl_owl2.fuzzydl.concept.concept import Concept
from fuzzy_dl_owl2.fuzzydl.concept.interface.has_weighted_concepts_interface import (
    HasWeightedConceptsInterface,
)
from fuzzy_dl_owl2.fuzzydl.concept.operator_concept import OperatorConcept
from fuzzy_dl_owl2.fuzzydl.util.constants import ConceptType
from fuzzy_dl_owl2.fuzzydl.util.util import Util


class SugenoIntegral(Concept, HasWeightedConceptsInterface):
    """Sugeno integral concept."""

    @typing.overload
    def __init__(self) -> None: ...

    @typing.overload
    def __init__(
        self, weights: typing.Optional[list[float]], concepts: list[Concept]
    ) -> None: ...

    def __init__(self, *args) -> None:
        assert len(args) in [0, 2]
        if len(args) == 0:
            self.__sugeno_init_1()
        else:
            trycast.checkcast(typing.Optional[list[float]], args[0])
            trycast.checkcast(list[Concept], args[1])
            self.__sugeno_init_2(*args)

    def __sugeno_init_1(self) -> None:
        Concept.__init__(self, ConceptType.SUGENO_INTEGRAL)
        HasWeightedConceptsInterface.__init__(self, None, [])

    def __sugeno_init_2(
        self, weights: typing.Optional[list[float]], concepts: list[Concept]
    ) -> None:
        Concept.__init__(self, ConceptType.SUGENO_INTEGRAL)
        HasWeightedConceptsInterface.__init__(self, weights, concepts)

        if weights is not None:
            if len(weights) != len(concepts):
                Util.error(
                    "Error: The number of weights and the number of concepts should be the same"
                )
            self.name = self.compute_name()
        else:
            self.weights: list[float] = []


    def clone(self) -> typing.Self:
        return SugenoIntegral(self.weights[:], [c for c in self.concepts])

    def compute_atomic_concepts(self) -> set[Concept]:
        concept_list: set[Concept] = set()
        for c in self.concepts:
            concept_list.update(c.compute_atomic_concepts())
        return concept_list

    def get_roles(self) -> set[str]:
        role_list: set[str] = set()
        for c in self.concepts:
            role_list.update(c.get_roles())
        return role_list

    def replace(self, a: Concept, c: Concept) -> Concept:
        return -SugenoIntegral(self.weights, [ci.replace(a, c) for ci in self.concepts])

    def compute_name(self) -> str:
        return f"(sugeno ({' '.join(map(str, self.weights))}) ({' '.join(map(str, self.concepts))}))"

    def __neg__(self) -> Concept:
        return OperatorConcept.not_(self)

    def __and__(self, value: typing.Self) -> typing.Self:
        return OperatorConcept.and_(self, value)

    def __or__(self, value: typing.Self) -> typing.Self:
        return OperatorConcept.or_(self, value)

    def __hash__(self) -> int:
        return hash(str(self))
