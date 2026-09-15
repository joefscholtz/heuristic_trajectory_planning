from pathlib import Path
from .core import BaseIndividual


class SE2Individual(BaseIndividual):
    def __init__(self, xyt_coords: list[tuple[float, float, float]]):
        super().__init__()
        self.xyt = xyt_coords

    def get_path_coordinates(self) -> tuple[list[float], list[float]]:
        x, y, theta = map(list, zip(*self.xyt))
        return x, y
