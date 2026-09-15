from pathlib import Path
import config_pb2
from .core import AnalysisClass, register_analysis
from map_handler import MapHandler
import matplotlib.pyplot as plt


@register_analysis("type.googleapis.com/htp.config.PrintTrajOnMapParams")
class PrintTrajOnMap(AnalysisClass):
    def __init__(self, payload, global_config):
        params = config_pb2.PrintTrajOnMapParams()
        payload.Unpack(params)
        self.map_yaml_path = params.map_yaml_path
        self.subsample_factor = params.subsample_factor
        self.plot_pause_time_s = params.plot_pause_time_s

        map = MapHandler.load_map_from_yaml(Path(self.map_yaml_path).resolve())
        if self.subsample_factor > 1:
            self.map = map.discretize(factor=self.subsample_factor)
        else:
            self.map = map
        self.fig = None
        self.ax = None

    def __call__(self, generation_n: int, population: list):
        print(f"\n--- Generation {generation_n} ---")
        if self.fig is None:
            plt.ion()  # Turn on interactive mode
            self.fig, self.ax = plt.subplots(figsize=(10, 10))

        # Redraw the map
        self.map.plot(ax=self.ax, show=False)

        # Assumes both initialization_fn and selection_fn sort by fitness
        ind = population[0]
        x_coords, y_coords = ind.get_path_coordinates()
        self.ax.plot(
            x_coords,
            y_coords,
            color="blue",
            alpha=0.6,
            linewidth=2,
            marker="o",
        )

        self.ax.plot(
            x_coords[0],
            y_coords[0],
            color="red",
            marker="o",
            alpha=0.6,
        )

        self.ax.plot(
            x_coords[-1],
            y_coords[-1],
            color="red",
            marker="o",
            alpha=0.6,
        )

        # Update title for current generation
        self.ax.set_title(f"Generation {generation_n}")
        # Force the GUI to render the new frame without blocking
        if self.plot_pause_time_s > 0.0:
            plt.pause(self.plot_pause_time_s)
