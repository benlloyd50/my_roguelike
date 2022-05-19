"""Actions"""

from __future__ import annotations

from typing import TYPE_CHECKING
from os.path import dirname, abspath
from os import listdir

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        DIRECTORY = dirname(abspath(__file__))
        #TODO: Integrate into the game console 
        if engine._load_name.split(sep='/')[-1] in listdir(DIRECTORY + "/../saves/"):
            engine.save_as(filename=engine._load_name)
            print(f"{engine._load_name} saved successfully") 
        else: 
            filename = str(input("Please enter a name for your save game: "))
            if filename != "":
                engine.save_as(filename=DIRECTORY + "/../saves/" + filename + ".sav")
                print(f"{filename} saved successfully")
        
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.is_loc_walkable(dest_x, dest_y):
            return

        entity.move(self.dx, self.dy)
        engine.game_map.move_offset(dx=self.dx, dy=self.dy)