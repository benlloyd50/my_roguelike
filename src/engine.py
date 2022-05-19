""" The "Loorna" Engine, an engine that I love
Manages the game state internally handling gamemap, events, and entities
"""
from typing import Any, Iterable, Set
from tcod.context import Context
from tcod.console import Console
from state_handlers import StateHandler
from actions import MovementAction, EscapeAction

import pickle
import lzma

from gamemap import GameMap
from entity import Entity

class Engine:
    def __init__(self, entities : Set[Entity], game_map: GameMap, player : Entity, state_handler : StateHandler, _load_name : str = ""):
        self.entities = entities
        self.game_map = game_map
        self.game_map.move_camera_to_player(player.x, player.y)
        self.player = player
        self.state_handler = state_handler
        self._load_name = _load_name


    def handle_events(self, events: Iterable[Any], context: Context) -> None:
        for event in events:
            context.convert_event(event)  # Sets tile coordinates for mouse events.
            print(event)  # Print event names and attributes.
            
            action = self.state_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)


    def render(self, console: Console, context: Context) -> None:
        """Draws gamemap, which draws entities internally"""
        self.game_map.render(console=console)
        context.present(console=console)  # Show the console.
        console.clear()


    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)