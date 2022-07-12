"""
The "Loorna" Engine, an engine that I love
Manages the game state internally handling gamemap, events, and entities
"""
from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING, Any, Iterable

from tcod.console import Console

from state_handlers import MainGameStateHandler

if TYPE_CHECKING:
    from camera import Camera
    from entity import Actor
    from gamemap import GameMap
    from state_handlers import StateHandler

class Engine:
    game_map: GameMap
    camera: Camera

    def __init__(self, player: Actor, loadname: str = ""):
        self.state_handler: StateHandler = MainGameStateHandler(self)
        self.player = player
        self.loadname = loadname

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            print(event)  # Print event names and attributes.

            action = self.state_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console: Console) -> None:
        """Draws gamemap, which draws entities internally"""
        self.camera.center_on_position(self.player.x, self.player.y)
        self.camera.render(console, self.game_map)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
