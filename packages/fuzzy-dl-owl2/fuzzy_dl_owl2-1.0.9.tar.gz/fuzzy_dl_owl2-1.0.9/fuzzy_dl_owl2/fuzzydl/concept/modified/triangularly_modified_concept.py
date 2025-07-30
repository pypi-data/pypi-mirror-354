from __future__ import annotations

import typing

from fuzzy_dl_owl2.fuzzydl.concept.concept import Concept
from fuzzy_dl_owl2.fuzzydl.concept.modified.modified_concept import ModifiedConcept
from fuzzy_dl_owl2.fuzzydl.concept.operator_concept import OperatorConcept
from fuzzy_dl_owl2.fuzzydl.modifier.modifier import Modifier


class TriangularlyModifiedConcept(ModifiedConcept):

    """Fuzzy concept modified with a triangular modifier."""

    def __init__(self, c: Concept, mod: Modifier) -> None:
        super().__init__(c, mod)

    def clone(self) -> typing.Self:
        return TriangularlyModifiedConcept(self.curr_concept, self.modifier)

    def replace(self, a: Concept, c: Concept) -> Concept:
        return -TriangularlyModifiedConcept(
            self.curr_concept.replace(a, c), self.modifier
        )

    def __neg__(self) -> Concept:
        return OperatorConcept.not_(self)

    def __and__(self, value: typing.Self) -> typing.Self:
        return OperatorConcept.and_(self, value)

    def __or__(self, value: typing.Self) -> typing.Self:
        return OperatorConcept.or_(self, value)

    def __hash__(self) -> int:
        return hash(str(self))
