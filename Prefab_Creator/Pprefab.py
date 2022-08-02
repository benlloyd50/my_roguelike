from dataclasses import dataclass
from numpy import ndarray

@dataclass
class Prefab:
    gamemap: ndarray
    source_pts: list
    tags: list
    name: str

    @property
    def width(self) -> int:
        return self.gamemap.shape[0]

    @property
    def height(self) -> int:
        return self.gamemap.shape[1]