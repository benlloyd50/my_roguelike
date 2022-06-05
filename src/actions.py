"""Actions"""

from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
from os.path import dirname, abspath
from os import listdir

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        # return self.entity.gamemap.engine
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        DIRECTORY = dirname(abspath(__file__))
        #TODO: Integrate into the game console 
        if self.engine._loadname.split(sep='/')[-1] in listdir(DIRECTORY + "/../saves/"):
            self.engine.save_as(filename=self.engine._loadname)
            print(f"{self.engine._loadname} saved successfully") 
        else: 
            filename = str(input("Please enter a name for your save game: "))
            if filename != "":
                self.engine.save_as(filename=DIRECTORY + "/../saves/" + filename + ".sav")
                print(f"{filename} saved successfully")
        
        raise SystemExit()


class WaitAction(Action):
    def perform(self) -> None:
        pass


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Return action's destination"""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at the dest if there is one"""
        return self.engine.game_map.get_blocking_entity_at_loc(*self.dest_xy)
    
    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at the dest if there is one"""
        return self.engine.game_map.get_actor_at_loc(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor: 
            return MeleeAction(self.entity, dx=self.dx, dy=self.dy).perform()
        else:
            return MovementAction(self.entity, dx=self.dx, dy=self.dy).perform()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target: #no actor returned
            return

        print(f"{target.name} was kicked")


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        if not self.engine.game_map.is_loc_walkable(*self.dest_xy):
            return

        self.entity.move(self.dx, self.dy)