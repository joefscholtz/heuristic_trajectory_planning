import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
import heuristic_trajectory_planning as htp

if __name__ == "__main__":
    map = htp.map_handler.MapHandler.load_map_from_yaml(
        (script_dir / "../config/map/turtlebot3_map.yaml").resolve()
    )
    map.plot()
    downsampled_grid = map.discretize(factor=4)
    downsampled_grid.plot()
