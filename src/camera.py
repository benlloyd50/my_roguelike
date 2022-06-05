from __future__ import annotations

import tile_types
from typing import Tuple
from numpy import select 
from gamemap import GameMap
from tcod.console import Console

class Camera:
    world_offset_x: int 
    world_offset_y: int

    def __init__(self, width: int, height: int, x: int = 5, y: int = 1) -> None:
        self.width = width
        self.height = height
        #Where to place the camera on the console screen
        self.screen_pos_x = x
        self.screen_pos_y = y

    @property
    def last_x_position(self) -> int:
        return self.world_offset_x + self.width

    @property
    def last_y_position(self) -> int:
        return self.world_offset_y + self.height

    def center_on_position(self, x: int, y: int) -> None:
        """Set the camera to have the player (x,y) be the center of the screen
        x and y should be world coordinates"""
        center_x = int(self.width / 2) + 1
        center_y = int(self.height / 2) + 1
        self.world_offset_x = x - center_x
        self.world_offset_y = y - center_y

    def render(self, console: Console, gamemap: GameMap) -> None:
        console.rgb[self.screen_pos_x: self.screen_pos_x + self.width, self.screen_pos_y :self.screen_pos_y + self.height] = select(
            condlist=[gamemap.conditions[self.world_offset_x : self.last_x_position, self.world_offset_y : self.last_y_position]],
            choicelist=[gamemap.tiles[self.world_offset_x : self.last_x_position, self.world_offset_y : self.last_y_position]['sprite']],
            default=tile_types.SHROUD,
        )

        for e in gamemap.entities:
            cam_x, cam_y = self.world_position_to_camera_positon(e.x, e.y)
            if cam_x == -1 and cam_y == -1:
                continue
            console.print(cam_x, cam_y, e.char, fg=e.color)

    def world_position_to_camera_positon(self, x: int, y: int) -> Tuple(int, int):
        """Converts world position to camera coordinates if in camera view otherwise returns (-1, -1)"""
        #check if world pos is currently visible to the camera, otherwise it has no world position
        if not (self.world_offset_x <= x < self.last_x_position and self.world_offset_y <= y < self.last_y_position):
            return (-1, -1)
        #convert to cam position
        return (x - self.world_offset_x + self.screen_pos_x, y - self.world_offset_y + self.screen_pos_y)

    def move_offset(self, dx: int, dy: int) -> None:
        """Move the x and y offsets of the camera by (dx, dy) tiles""" 
        self.x_offset += dx
        self.y_offset += dy