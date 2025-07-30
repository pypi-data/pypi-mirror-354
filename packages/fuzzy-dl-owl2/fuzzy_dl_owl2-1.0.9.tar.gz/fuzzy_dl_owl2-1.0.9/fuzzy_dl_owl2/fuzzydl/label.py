import typing

from fuzzy_dl_owl2.fuzzydl.concept.concept import Concept
from fuzzy_dl_owl2.fuzzydl.degree.degree import Degree
from fuzzy_dl_owl2.fuzzydl.degree.degree_numeric import DegreeNumeric


class Label:
    """
    Label (weighted concept used in created individuals)
    """

    def __init__(self, concept: Concept, weight: Degree) -> None:
        self.concept: Concept = concept
        # Weight in [0,1]
        self.weight: Degree = weight

    @staticmethod
    def weights_equal(w1: Degree, w2: Degree) -> bool:
        """
        Checks if two degrees are equal
        """
        if not w1.__class__ == w2.__class__:
            return False
        return (
            not w1.is_numeric()
            or typing.cast(DegreeNumeric, w1).get_numerical_value()
            == typing.cast(DegreeNumeric, w2).get_numerical_value()
        )

    def __str__(self) -> str:
        return f"{self.concept} {self.weight}"

    def __eq__(self, cw: typing.Self) -> bool:
        if self.concept != cw.concept:
            return False
        return self.weights_equal(self.weight, cw.weight)

    def __ne__(self, cw: typing.Self) -> bool:
        return not (self == cw)
