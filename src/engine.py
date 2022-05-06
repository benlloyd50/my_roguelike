""" The "Loorna" Engine, an engine that I love
Manages the game state internally handling gamemap, events, and entities
"""
from tcod.context import Context
from tcod.console import Console
import tcod.event

from gamemap import GameMap
from entity import Entity

MOVECOMMANDS = {
    tcod.event.KeySym.w: (0, -1),
    tcod.event.KeySym.a: (-1, 0),
    tcod.event.KeySym.s: (0, 1),
    tcod.event.KeySym.d: (1, 0),
}

class Engine:
    def __init__(self, entities, game_map, player):
        self.entities = entities
        self.game_map = game_map
        self.player = player

    def handle_events(self, events, context):
        for event in events:
            context.convert_event(event)  # Sets tile coordinates for mouse events.
            #print(event)  # Print event names and attributes.
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()
            elif isinstance(event, tcod.event.KeyDown):
                if event.sym in MOVECOMMANDS:
                    if self.game_map.is_loc_walkable(self.player.x + MOVECOMMANDS[event.sym][0], self.player.y + MOVECOMMANDS[event.sym][1]):
                        self.player.move(MOVECOMMANDS[event.sym][0], MOVECOMMANDS[event.sym][1])
                    else:
                        print("You can't walk")
                elif event.sym is tcod.event.KeySym.ESCAPE:
                    raise SystemExit()

    def render(self, console: Console, context: Context):
        """Draws gamemap, which draws entities internally"""
        console.clear()
        self.game_map.render(console=console)
        context.present(console=console)  # Show the console.

