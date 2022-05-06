from typing import Tuple, TypeVar
T = TypeVar('T', bound="Entity")


class Entity:
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        render_priority: int = 10, #0 = player, 1 = entities, 10 = default 
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.render_priority = render_priority

    def __ge__(self: T, other: T) -> bool:
        return self.render_priority >= other.render_priority

    def __lt__(self: T, other: T) -> bool:
        return self.render_priority < other.render_priority

    def move(self, dx: int, dy: int):
        """Move entity position relative to where it stands"""
        self.x += dx
        self.y += dy