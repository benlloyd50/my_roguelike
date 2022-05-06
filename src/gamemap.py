from __future__ import annotations

import numpy as np #type: ignore
from typing import List
import tile_types
from tcod.console import Console
from entity import Entity


class GameMap:
    def __init__(self, width: int, height: int, entities: List[Entity]):
        self.width, self.height = width, height

        self.tiles = np.full((self.width, self.height), fill_value=tile_types.water, order="F")
        self.conditions = np.full((self.width, self.height), fill_value=True, order="F")
        self.entities = entities

    @property
    def gamemap(self) -> GameMap:
        return self
    
    def render(self, console: Console) -> None:
        console.rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.conditions],
            choicelist=[self.tiles['sprite']],
            default=tile_types.SHROUD,
        )

        self.entities = sorted(self.entities, reverse=True)   #sorts entity by render priority, lowest first
        for e in self.entities:
            #allows bg to be none, so we could take the color of the tile instead
            console.print(e.x, e.y, e.char, fg=e.color)

    def is_loc_walkable(self, x: int, y: int) -> bool:
        return self.game_map[x, y]['walkable'] and self.inbounds(x, y)

    def inbounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
