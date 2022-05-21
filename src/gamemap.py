from __future__ import annotations

from typing import Iterable, Iterator, Tuple, Optional, TYPE_CHECKING
from tcod.console import Console

from entity import Actor
import numpy as np #type: ignore
import colors
import tile_types

if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine

class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity]):
        self.width, self.height = width, height
        self.engine = engine

        self.cam_width = 81 
        self.cam_height = 31 
        self.cam_x_offset = 5 
        self.cam_y_offset = 1 
        
        self._x_offset = 0 #is the left most position of what is shown on the camera
        self._y_offset = 0 #is the top most position of what is show on the camera

        self.tiles = np.full((self.width, self.height), fill_value=tile_types.water, order="F")
        self.conditions = np.full((self.width, self.height), fill_value=True, order="F")
        self.entities = set(entities)

    @property
    def actors(self) -> Iterator[Actor]:
        yield from(
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

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
        #Make this less wordy fuck
        console.rgb[self.cam_x_offset : self.cam_x_offset + self.cam_width, self.cam_y_offset :self.cam_y_offset + self.cam_height] = np.select(
            condlist=[self.conditions[self.x_offset : self.last_x_position, self.y_offset : self.last_y_position]],
            choicelist=[self.tiles[self.x_offset : self.last_x_position, self.y_offset : self.last_y_position]['sprite']],
            default=tile_types.SHROUD,
        )

        self.entities = sorted(self.entities, reverse=True)   #sorts entity by render priority, lowest first
        for e in self.entities:
            #allows bg to be none, so we could take the color of the tile instead
            cam_x, cam_y = self.world_position_to_camera_positon(e.x, e.y)
            if cam_x == -1 and cam_y == -1:
                continue
            # compile list of entities inside cam's view somehow
            # potentially update list as new tiles are explored?
            console.print(cam_x, cam_y, e.char, fg=e.color)
        
        console.draw_frame(
            x=self.cam_x_offset - 1,
            y=0,
            width=self.cam_width+2,
            height=self.cam_height+2,
            decoration="╔═╗║ ║╚═╝",
            bg=colors.dark_brown,
            fg=colors.light_brown,
            clear=False,
        )

    def move_camera_to_player(self, x: int, y: int):
        """Set the camera to have the player (x,y) be the center of the screen
        x and y should be world coordinates"""
        center_x = int(self.cam_width / 2) + 1
        center_y = int(self.cam_height / 2) + 1
        self.x_offset = x - center_x
        self.y_offset = y - center_y

    def world_position_to_camera_positon(self, x: int, y: int) -> Tuple(int, int):
        """Converts world position to camera coordinates if in camera view otherwise returns (-1, -1)"""
        #check if world pos is currently visible to the camera, otherwise it has no world position
        if not (self.x_offset <= x < self.last_x_position and self.y_offset <= y < self.last_y_position):
            return (-1, -1)
        #convert to cam position
        return (x - self.x_offset + self.cam_x_offset, y - self.y_offset + self.cam_y_offset)

    def move_offset(self, dx: int, dy: int) -> None:
        """Move the x and y offsets of the camera by (dx, dy) tiles""" 
        self.x_offset += dx
        self.y_offset += dy

    def get_blocking_entity_at_loc(self, loc_x: int, loc_y: int) -> Optional[Entity]:
        for e in self.entities:
            if ( 
                e.blocks_movement
                and e.x == loc_x
                and e.y == loc_y
            ) :
                return e
        return None

    def get_actor_at_loc(self, x: int, y: int) -> Optional[Actor]:
        for a in self.actors:
            if a.x == x and a.y == y:
                return a
        return None

    def is_loc_walkable(self, x: int, y: int) -> bool:
        return (
            self.inbounds(x, y) 
            and self.tiles[x, y]['walkable'] 
            and self.get_blocking_entity_at_loc(x, y) is None
        )

    def inbounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
