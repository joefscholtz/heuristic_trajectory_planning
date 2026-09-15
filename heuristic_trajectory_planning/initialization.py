import config_pb2
from .core import InitializationStrategy, register_initialization

# @register_initialization("type.googleapis.com/htp.config.RandomTrajsSE2Params")
# class RandomTrajsSE2(InitializationStrategy):
#     def __init__(self, payload, global_config):
#         params = config_pb2.TournamentSelectionParams()
#         payload.Unpack(params)
#         self.tournament_size = params.tournament_size
#
#     def __call__(self) -> list[BaseIndividual]:
#         return [
#             DummyIndividual([(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)]),
#             DummyIndividual([(0.0, 0.5), (1.5, 1.5), (0.5, 0.5)]),
#         ]
