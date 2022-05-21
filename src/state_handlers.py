"""
State Handler Class
Contains different states for throughout the game, picking up from part 6 to make changes
"""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, WaitAction, BumpAction

if TYPE_CHECKING:
    from engine import Engine
"""
Commands should be mappable to work with only number keys,
some low usage commands may be outsourced to keyboard
"""
MOVE_KEYS = {
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
ESCAPE_KEYS = [
    tcod.event.K_ESCAPE,
    tcod.event.KeySym.N0,
]
DEBUG_KEYS = {
    tcod.event.KeySym.k: 0,
}
WAIT_KEYS = [
    tcod.event.KeySym.p,
]


class StateHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        """Handles events differently based on the state"""
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()


class MainGameStateHandler(StateHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()
            # Handle Enemy Turns
            # Update FOV


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        player = self.engine.player

        match key:
            case key if key in MOVE_KEYS:
                action = BumpAction(player, *MOVE_KEYS[key])
            case key if key in WAIT_KEYS:
                action = WaitAction(player)
            case key if key in ESCAPE_KEYS:
                action = EscapeAction(player)

        # No valid key was pressed
        return action


class GameOverStateHandler(StateHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        player = self.engine.player

        if key in ESCAPE_KEYS:
            action = EscapeAction(player)

        # No valid key was pressed
        return action