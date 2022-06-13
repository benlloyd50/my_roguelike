"""
Gamemap is the container for everything that exists in the world
There will be a parent added in the future for sub maps such as caves
"""
from __future__ import annotations

from typing import Iterable, Iterator, Tuple, Optional, TYPE_CHECKING
from tcod.console import Console

from entity import Actor
import numpy as np #type: ignore
import colors
import tile_types

if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine

class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity]):
        self.width, self.height = width, height
        self.engine = engine

        self.tiles = np.full((self.width, self.height), fill_value=tile_types.water, order="F")
        self.conditions = np.full((self.width, self.height), fill_value=True, order="F")
        self.entities = set(entities)

    @property
    def actors(self) -> Iterator[Actor]:
        yield from(
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_blocking_entity_at_loc(self, loc_x: int, loc_y: int) -> Optional[Entity]:
        for e in self.entities:
            if ( 
                e.blocks_movement
                and e.x == loc_x
                and e.y == loc_y
            ) :
                return e
        return None

    def get_actor_at_loc(self, x: int, y: int) -> Optional[Actor]:
        for a in self.actors:
            if a.x == x and a.y == y:
                return a
        return None

    def is_loc_walkable(self, x: int, y: int) -> bool:
        return (
            self.inbounds(x, y) 
            and self.tiles[x, y]['walkable'] 
            and self.get_blocking_entity_at_loc(x, y) is None
        )

    def inbounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
