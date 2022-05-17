""" The "Loorna" Engine, an engine that I love
Manages the game state internally handling gamemap, events, and entities
"""
from tcod.context import Context
from tcod.console import Console
import tcod.event

MOVECOMMANDS = {
    tcod.event.KeySym.w: (0, -1),
    tcod.event.KeySym.a: (-1, 0),
    tcod.event.KeySym.s: (0, 1),
    tcod.event.KeySym.d: (1, 0),
}
DEBUGCOMMANDS = {
    tcod.event.KeySym.k: 0,
}

class Engine:
    def __init__(self, entities, game_map, player):
        self.entities = entities
        self.game_map = game_map
        self.game_map.move_camera_to_player(player.x, player.y)
        self.player = player

    def handle_events(self, events, context):
        for event in events:
            context.convert_event(event)  # Sets tile coordinates for mouse events.
            #print(event)  # Print event names and attributes.
            #extrapolate below to event_handler class that controls state of game
            match event:
                case tcod.event.KeyDown(sym=sym) if sym in DEBUGCOMMANDS:
                    print(f"{self.player.x = }, {self.player.y = }")
                case tcod.event.Quit():
                    raise SystemExit()
                case tcod.event.KeyDown(sym=sym) if sym in MOVECOMMANDS:
                    if self.game_map.is_loc_walkable(self.player.x + MOVECOMMANDS[sym][0], self.player.y + MOVECOMMANDS[sym][1]):
                        self.player.move(MOVECOMMANDS[sym][0], MOVECOMMANDS[sym][1])
                        self.game_map.move_offset(MOVECOMMANDS[sym][0], MOVECOMMANDS[sym][1])
                    else:
                        print("You can't walk there")
                case tcod.event.KeyDown(sym=sym) if sym is tcod.event.KeySym.ESCAPE:
                    raise SystemExit() 

    def render(self, console: Console, context: Context):
        """Draws gamemap, which draws entities internally"""
        console.clear()
        self.game_map.render(console=console)
        context.present(console=console)  # Show the console.
