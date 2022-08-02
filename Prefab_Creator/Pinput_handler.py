""" Input Handler
    Reads in events to do certain functions
    Also handles most of the state for the app
"""
from enum import Enum, auto

import tcod
import numpy as np

import Ptile_types as tile_types
from Pmessagelog import MessageLog
from Pprefab import Prefab


class InputMode(Enum):
    sourcepoint = auto()
    wall = auto()
    floor = auto()


class InputHandler(tcod.event.EventDispatch):
    def __init__(self, prefab: Prefab) -> None:
        self.prefab = prefab
        self._mode = InputMode.sourcepoint
        self.log = MessageLog(10)

    @property
    def gamemap(self):
        return self.prefab.gamemap

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
        self.log.add(f"Mode changed to {self.mode}")
    
    def is_tile_in_room(self, x: int, y: int) -> bool:
        return (0 <= x < self.prefab.width) and (0 <= y < self.prefab.height)

    def render(self, console: tcod.Console):
        console.clear()
        #Room
        console.rgb[:self.prefab.width, :self.prefab.height] = self.gamemap['sprite']
        #Info
        console.draw_frame(x=0, y=console.rgb.shape[1] - 12, width=console.rgb.shape[0], height=12)
        for idx, msg in enumerate(self.log.recent):
            console.print(
                x=1,
                y=console.rgb.shape[1] - 11 + idx,
                string=msg
                )

    def handle_event(self, event: tcod.event.Event) -> None:
        self.dispatch(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown):
        if event.button == tcod.event.BUTTON_LEFT:
            if self.is_tile_in_room(event.tile.x, event.tile.y):
                self.place_tile(event.tile.x, event.tile.y)
            else:
                self.log.add(f"Cannot act on {event.tile.x}, {event.tile.y}")
        elif event.button == tcod.event.BUTTON_RIGHT:
            if self.mode == InputMode.sourcepoint and self.gamemap[event.tile.x, event.tile.y] == tile_types.source_tile:
                self.gamemap[event.tile.x, event.tile.y] = tile_types.remove_me
                self.prefab.source_pts.remove((event.tile.x, event.tile.y))
                
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        match event.sym:
            case tcod.event.K_1:
                self.mode = InputMode.sourcepoint
            case tcod.event.K_2:
                self.mode = InputMode.wall
            case tcod.event.K_3:
                self.mode = InputMode.floor
            case tcod.event.K_s:
                self.log.add(f"{self.prefab.source_pts = }")
            case tcod.event.K_RETURN:
                print("Apply finishing touches now")
            case tcod.event.K_ESCAPE:
                #TODO: move saving out of here
                np.save(f"assets/prefabs/{self.prefab.name}.npy", self.prefab.gamemap)
                raise SystemExit()

    def place_tile(self, x: int, y: int):
        if self.mode == InputMode.sourcepoint:
            self.gamemap[x, y] = tile_types.source_tile
            self.prefab.source_pts.append((x, y))
        elif self.mode == InputMode.wall:
            self.gamemap[x, y] = tile_types.gray_wall
        elif self.mode == InputMode.floor:
            self.gamemap[x, y] = tile_types.gray_floor

    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()
    