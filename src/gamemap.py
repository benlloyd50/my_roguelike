import numpy as np #type: ignore
from typing import Tuple
import colors as clr
from tcod.console import Console

#a list of info useful for making maps that resembles the console.rgb type
tile_graphic = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B")
    ]
)

map_tile = np.dtype(
    [
        ("walkable", np.bool), 
        ("sprite", tile_graphic)
    ]
)


class GameMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.game_map = np.full((width, height), fill_value=water, order="F")
        print(self.game_map.dtype)
        self.conditions = np.full((self.width, self.height), fill_value=True, order="F")
        #self.conditions2 = np.full((self.width, self.height), fill_value=True, order="F")

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=self.conditions,
            choicelist=self.game_map["sprite"],
            default=water['sprite'],
        ) 


#sprite resembles the tile_graphic np type defined at top of class
def new_tile(
    *,
    walkable: bool,
    sprite: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    return np.array((walkable, sprite), dtype=map_tile)

water = new_tile(walkable=False, sprite=(ord("~"), clr.light_blue, clr.murky_blue))