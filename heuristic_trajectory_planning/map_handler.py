import yaml
import numpy as np
from PIL import Image
from enum import Enum
from pathlib import Path
from dataclasses import dataclass

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

OCC_GRID_UNKNOWN = -1
OCC_GRID_FREE = 0
OCC_GRID_OCCUPIED = 100


class MapMode(Enum):
    TRINARY = "trinary"
    SCALE = "scale"
    RAW = "raw"


@dataclass
class MapOrigin:
    x: float
    y: float
    yaw: float


@dataclass
class MapInfo:
    width: int
    height: int
    resolution: float
    origin: MapOrigin


@dataclass
class LoadParameters:
    image_file_path: Path
    resolution: float
    origin: list[float]
    free_thresh: float
    occupied_thresh: float
    mode: MapMode
    negate: bool


@dataclass
class OccupancyGrid:
    info: MapInfo
    data: np.ndarray  # 2D numpy array of int8, shape: [height, width]

    def discretize(self, factor: int) -> "OccupancyGrid":
        """
        Subsamples the map by aggregating NxN blocks into single cells.
        Uses max-pooling to prioritize obstacles over free space.

        Args:
            factor (int): The scaling factor (e.g., 2 means half the resolution).
        """
        if factor <= 1:
            return self

        h, w = self.data.shape
        new_h = int(np.ceil(h / factor))
        new_w = int(np.ceil(w / factor))

        # Pad array so dimensions are perfect multiples of the factor
        pad_h = (new_h * factor) - h
        pad_w = (new_w * factor) - w

        if pad_h > 0 or pad_w > 0:
            padded = np.pad(
                self.data,
                ((0, pad_h), (0, pad_w)),
                mode="constant",
                constant_values=OCC_GRID_UNKNOWN,
            )
        else:
            padded = self.data

        # Reshape into blocks and apply max pooling
        # Max-pooling works perfectly here because: OCC_GRID_UNKNOWN (-1) < FREE (0) < OCCUPIED (100)
        # It guarantees that an obstacle overrides free space, and known space overrides unknown.
        reshaped = padded.reshape(new_h, factor, new_w, factor)
        downsampled_data = reshaped.max(axis=(1, 3)).astype(np.int8)

        new_info = MapInfo(
            width=new_w,
            height=new_h,
            resolution=self.info.resolution * factor,
            origin=self.info.origin,  # Origin coordinate (bottom-left) remains identical
        )

        return OccupancyGrid(info=new_info, data=downsampled_data)

    def plot(self):
        """Visualizes the 2D map using Matplotlib."""
        if plt is None:
            raise ImportError(
                "matplotlib is required to plot. Run: pip install matplotlib"
            )

        # Map to visual colors [0.0 = Black, 1.0 = White, 0.5 = Gray/Unknown]
        vis_img = np.zeros_like(self.data, dtype=np.float32)

        vis_img[self.data == OCC_GRID_UNKNOWN] = 0.5
        vis_img[self.data == OCC_GRID_FREE] = 1.0
        vis_img[self.data == OCC_GRID_OCCUPIED] = 0.0

        # Handle intermediate scale values smoothly
        scale_mask = (self.data > OCC_GRID_FREE) & (self.data < OCC_GRID_OCCUPIED)
        vis_img[scale_mask] = 1.0 - (self.data[scale_mask] / 100.0)

        plt.figure(figsize=(10, 10))

        # origin='lower' because row 0 in our flipped matrix represents the bottom-left coordinate
        extent = [
            self.info.origin.x,
            self.info.origin.x + self.info.width * self.info.resolution,
            self.info.origin.y,
            self.info.origin.y + self.info.height * self.info.resolution,
        ]

        plt.imshow(vis_img, cmap="gray", origin="lower", extent=extent)

        plt.title(
            f"Occupancy Grid: {self.info.width}x{self.info.height} | Res: {self.info.resolution:.3f} m/px"
        )
        plt.xlabel("X (meters)")
        plt.ylabel("Y (meters)")
        plt.show()


class MapHandler:
    @staticmethod
    def _load_map_yaml(yaml_path: Path) -> LoadParameters:
        yaml_path = yaml_path.expanduser().resolve()

        with open(yaml_path, "r") as f:
            doc = yaml.safe_load(f)

        image_file_name = doc.get("image")
        if not image_file_name:
            raise ValueError("The 'image' tag in the YAML file is empty or missing.")

        image_path = Path(image_file_name).expanduser()
        if not image_path.is_absolute():
            image_path = (yaml_path.parent / image_path).resolve()

        origin = doc.get("origin")
        if not origin or len(origin) != 3:
            raise ValueError(
                f"The 'origin' tag should have 3 elements, got {len(origin) if origin else 0}"
            )

        mode_str = doc.get("mode", "trinary").lower()
        try:
            mode = MapMode(mode_str)
        except ValueError:
            raise ValueError(f"Invalid map mode: {mode_str}")

        return LoadParameters(
            image_file_path=image_path,
            resolution=float(doc["resolution"]),
            origin=[float(x) for x in origin],
            free_thresh=float(doc["free_thresh"]),
            occupied_thresh=float(doc["occupied_thresh"]),
            mode=mode,
            negate=bool(doc.get("negate", False)),
        )

    @staticmethod
    def _load_map_from_file(params: LoadParameters) -> OccupancyGrid:
        img = Image.open(params.image_file_path)
        width, height = img.size

        has_alpha = img.mode in ("RGBA", "LA", "PA")
        alpha_array = None
        if has_alpha:
            alpha_array = np.array(img.split()[-1])

        gray = img.convert("L")
        gray_matrix = np.array(gray, dtype=np.float32)

        result = np.full((height, width), OCC_GRID_UNKNOWN, dtype=np.int8)

        if params.mode in (MapMode.TRINARY, MapMode.SCALE):
            normalized = gray_matrix / 255.0

            if not params.negate:
                normalized = 1.0 - normalized

            occupied_mask = normalized >= params.occupied_thresh
            free_mask = normalized <= params.free_thresh

            result[occupied_mask] = OCC_GRID_OCCUPIED
            result[free_mask] = OCC_GRID_FREE

            if params.mode == MapMode.SCALE:
                in_between_mask = (normalized > params.free_thresh) & (
                    normalized < params.occupied_thresh
                )
                if np.any(in_between_mask):
                    scaled_float = (
                        (normalized - params.free_thresh)
                        / (params.occupied_thresh - params.free_thresh)
                    ) * 100.0
                    result[in_between_mask] = np.round(
                        scaled_float[in_between_mask]
                    ).astype(np.int8)

            if has_alpha and alpha_array is not None:
                result[alpha_array < 255] = OCC_GRID_UNKNOWN

        elif params.mode == MapMode.RAW:
            result = gray_matrix.astype(np.int8)
            out_of_bounds = (result < OCC_GRID_FREE) | (result > OCC_GRID_OCCUPIED)
            result[out_of_bounds] = OCC_GRID_UNKNOWN

        # Flip image vertically to set origin at bottom-left, matching ROS coordinate frames
        flipped = np.flipud(result)

        map_info = MapInfo(
            width=width,
            height=height,
            resolution=params.resolution,
            origin=MapOrigin(
                x=params.origin[0], y=params.origin[1], yaw=params.origin[2]
            ),
        )

        return OccupancyGrid(info=map_info, data=flipped)

    @classmethod
    def load_map_from_yaml(cls, yaml_path: Path | str) -> OccupancyGrid:
        yaml_path = Path(yaml_path)
        params = cls._load_map_yaml(yaml_path)
        return cls._load_map_from_file(params)
