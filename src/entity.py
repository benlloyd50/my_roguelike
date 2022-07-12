from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Optional, Tuple, TypeVar

if TYPE_CHECKING:
    from gamemap import GameMap

T = TypeVar('T', bound="Entity")


class Entity:
    gamemap: GameMap

    def __init__(
        self,
        gamemap: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_priority: int = 10, #0 = player, 1 = entities, 10 = default 
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_priority = render_priority

        if gamemap:
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def __ge__(self: T, other: T) -> bool:
        return self.render_priority >= other.render_priority

    def __lt__(self: T, other: T) -> bool:
        return self.render_priority < other.render_priority

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, new_gamemap: Optional[GameMap] = None) -> None:
        """Place entity at new location, including gamemap transfers"""
        self.x = x
        self.y = y
        if new_gamemap: # if there was a gamemap, remove your trace in it and add it to the new one
            if hasattr(self, "gamemap"): #this will even swap if it was the same gamemap maybe there's a check for that
                self.gamemap.entities.remove(self)
            self.gamemap = new_gamemap
            new_gamemap.entities.add(self)

    def move(self, dx: int, dy: int):
        """Move entity position relative to where it stands"""
        self.x += dx
        self.y += dy


class Actor(Entity): #Sort of entities but they do more than that
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_priority=10,
        )

    @property
    def is_alive(self) -> bool:
        """Returns true as long as this actor can perform actions"""
        return True
