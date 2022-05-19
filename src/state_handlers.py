"""
State Handler Class
Contains different states for throughout the game
"""
from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction

"""
Commands should be mappable to work with only number keys,
some low usage commands may be outsourced to keyboard
"""

MOVECOMMANDS = {
    tcod.event.KeySym.w: (0, -1),
    tcod.event.KeySym.a: (-1, 0),
    tcod.event.KeySym.s: (0, 1),
    tcod.event.KeySym.d: (1, 0),
    #numbers
    tcod.event.KeySym.N8: (0, -1),
    tcod.event.KeySym.N4: (-1, 0),
    tcod.event.KeySym.N6: (1, 0),
    tcod.event.KeySym.N2: (0, 1),
}
ESCAPECOMMANDS = [
    tcod.event.K_ESCAPE,
    tcod.event.KeySym.N0,
]
DEBUGCOMMANDS = {
    tcod.event.KeySym.k: 0,
}

class StateHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        match key:
            case key if key in MOVECOMMANDS:
                action = MovementAction(*MOVECOMMANDS[key])

            case key if key in ESCAPECOMMANDS:
                action = EscapeAction()

        # No valid key was pressed
        return action