"""
State Handler Class
Contains different states for throughout the game
"""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Union
import tcod.event
import actions
from actions import Action, EscapeAction, WaitAction, BumpAction
import colors

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

ActionOrHandler = Union[Action, "StateHandler"]


class BaseStateHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> None:
        """Handles events differently based on the state"""
        state = self.dispatch(event)
        if isinstance(state, StateHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions"
        return self

    def on_render(self, console: tcod.Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()


class StateHandler(BaseStateHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> None:
        """Handles events if they are an action or state change"""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, StateHandler):
            return action_or_state
        if self.handle_action(action_or_state): #will handle every action but if true means a turn progressed
            if not self.engine.player.is_alive:
                return GameOverStateHandler(self.engine)
            return MainGameStateHandler(self.engine)
        return self

    def handle_action(self, action: Optional[Action]) -> bool:
        if action is None:
            return False 

        action.perform()
        return True

    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)


class MainGameStateHandler(StateHandler):
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


# class MenuTestStateHandler(StateHandler):
#     """A test for how making a menu may work"""
#     def on_render(self, console: tcod.Console) -> None:
#         super().on_render(console)

#         console.draw_frame(x=int(console.width / 2), y=25, width=50, height=20, title="TestMenu", bg=colors.light_blue)


#     def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
#         action: Optional[Action] = None
#         key = event.sym
#         player = self.engine.player

#         if key is tcod.event.KeySym.c:
#             return MainGameStateHandler(self.engine)
#         elif key is tcod.event.KeySym.j:
#             print("We do a little something")

#         return action


class GameOverStateHandler(StateHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        player = self.engine.player

        if key in ESCAPE_KEYS:
            action = EscapeAction(player)

        # No valid key was pressed
        return action