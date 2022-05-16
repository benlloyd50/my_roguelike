from __future__ import annotations

import numpy as np #type: ignore
from typing import List, Tuple
import tile_types
from tcod.console import Console
from entity import Entity


class GameMap:
    def __init__(self, width: int, height: int, entities: List[Entity]):
        self.width, self.height = width, height
        self.cam_width = 90 #draws 90 pixels starting from x_offset
        self.cam_height = 41
        self._x_offset = 0 #is the left most position of what is shown on the camera
        self._y_offset = 0 #is the top most position of what is show on the camera

        self.tiles = np.full((self.width, self.height), fill_value=tile_types.water, order="F")
        self.conditions = np.full((self.width, self.height), fill_value=True, order="F")
        self.entities = entities

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def x_offset(self):
        return self._x_offset

    @x_offset.setter
    def x_offset(self, value: int):
        if value < 0:
            self._x_offset = 0
        elif value > self.width - self.cam_width:
            self._x_offset = self.width - self.cam_width
        else:
            self._x_offset = value 

    @property
    def y_offset(self):
        return self._y_offset

    @y_offset.setter
    def y_offset(self, value: int):
        if value < 0:
            self._y_offset = 0
        elif value > self.height - self.cam_height:
            self._y_offset = self.height - self.cam_height
        else:
            self._y_offset = value 

    @property
    def last_x_position(self) -> int:
        return self.x_offset + self.cam_width

    @property
    def last_y_position(self) -> int:
        return self.y_offset + self.cam_height
    
    def render(self, console: Console) -> None:
        console.rgb[0:90, 0:41] = np.select(
            condlist=[self.conditions[self.x_offset : self.last_x_position, self.y_offset : self.last_y_position]],
            choicelist=[self.tiles[self.x_offset : self.last_x_position, self.y_offset : self.last_y_position]['sprite']],
            default=tile_types.SHROUD,
        )

        self.entities = sorted(self.entities, reverse=True)   #sorts entity by render priority, lowest first
        for e in self.entities:
            #allows bg to be none, so we could take the color of the tile instead
            #compile list of entities inside cam's view somehow
            # potentially update list as new tiles are explored?
            console.print(*self.world_position_to_camera_positon(e.x, e.y), e.char, fg=e.color)
    
    def world_position_to_camera_positon(self, x: int, y: int) -> Tuple(int, int):
        """Converts world position to camera coordinates if in camera view otherwise returns (-1, -1)"""
        #check if world pos is currently visible to the camera, otherwise it has no world position
        if not (self.x_offset <= x < self.last_x_position and self.y_offset <= y < self.last_y_position):
            return (-1, -1)
        #convert to cam position
        return (x - self.x_offset, y - self.y_offset)

    def move_offset(self, dx: int, dy: int):
        self.x_offset += dx
        self.y_offset += dy

    def is_loc_walkable(self, x: int, y: int) -> bool:
        return self.tiles[x, y]['walkable'] and self.inbounds(x, y)

    def inbounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
