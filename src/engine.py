""" The "Loorna" Engine, an engine that I love
Manages the game state internally handling gamemap, events, and entities
"""
from __future__ import annotations

from typing import Any, Iterable, TYPE_CHECKING
from tcod.context import Context
from tcod.console import Console
from state_handlers import MainGameStateHandler

import pickle
import lzma
if TYPE_CHECKING:
    from gamemap import GameMap
    from entity import Actor 
    from state_handlers import StateHandler

class Engine:
    game_map: GameMap

    def __init__(self, player: Actor, _loadname: str = ""):
        self.state_handler: StateHandler = MainGameStateHandler(self)
        self.player = player
        self._loadname = _loadname
        
    def handle_events(self, events: Iterable[Any], context: Context) -> None:
        for event in events:
            context.convert_event(event)  #gives the event information about the mouse 
            print(event)  # Print event names and attributes.
            
            action = self.state_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)


    def render(self, console: Console, context: Context) -> None:
        """Draws gamemap, which draws entities internally"""
        self.game_map.render(console)
        context.present(console)  # Show the console.
        console.clear()


    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)