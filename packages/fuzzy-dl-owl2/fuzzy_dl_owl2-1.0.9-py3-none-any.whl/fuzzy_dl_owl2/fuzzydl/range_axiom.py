from fuzzy_dl_owl2.fuzzydl.concept.concept import Concept


class RangeAxiom:
    """
    Role range axiom
    """

    def __init__(self, role: str, concept: Concept) -> None:
        self.role: str = role
        self.concept: Concept = concept
