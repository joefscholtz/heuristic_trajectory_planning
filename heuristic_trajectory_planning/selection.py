import config_pb2
from .core import SelectionStrategy, register_selection


@register_selection("type.googleapis.com/htp.config.TournamentSelectionParams")
class TournamentSelection(SelectionStrategy):
    def __init__(self, payload):
        params = config_pb2.TournamentSelectionParams()
        payload.Unpack(params)
        self.tournament_size = params.tournament_size

    def __call__(self, population: list, recombination: list, mutation: list) -> list:
        print(f"[Select] Running Tournament Selection (size: {self.tournament_size})")
        # TODO: Implement your actual tournament logic here
        return population


@register_selection("type.googleapis.com/htp.config.CustomSelectionParams")
class CustomSelection(SelectionStrategy):
    def __init__(self, payload):
        params = config_pb2.TournamentSelectionParams()
        payload.Unpack(params)
        self.tournament_size = params.tournament_size

    def __call__(self, population: list, recombination: list, mutation: list) -> list:
        return population
