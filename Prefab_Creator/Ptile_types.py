""" 
Tile types used for making maps in the Prefab Creator
These include some debug/misc tiles but tiles intended for the player to see should be copied to tile_types.py in the src folder
"""
from typing import Tuple
import Pcolors as clr
import numpy as np

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("sprite", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
    *,  
    walkable: int,
    transparent: int,
    sprite: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, sprite), dtype=tile_dt)


SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

water = new_tile(walkable=False, transparent=True, sprite=(ord("~"), clr.light_blue, clr.murky_blue))
grass = new_tile(walkable=True, transparent=True,sprite=(ord("\""), clr.light_green, clr.dark_green))
sand = new_tile(walkable=True, transparent=True, sprite=(ord("."), clr.light_brown, clr.yellow))
gray_wall = new_tile(walkable=False, transparent=False, sprite=(ord("*"), clr.light_brown, clr.brown))
gray_floor = new_tile(walkable=True, transparent=True, sprite=(ord("."), clr.gray_orange, clr.dark_gray))

remove_me = new_tile(walkable=False, transparent=False, sprite=(ord(' '), clr.testing_purple, clr.testing_purple))
source_tile = new_tile(walkable=False, transparent=False, sprite=(ord("+"), clr.testing_purple, clr.orange))