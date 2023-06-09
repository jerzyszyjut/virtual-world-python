import random

from virtual_world.config import Config
from virtual_world.organisms.collision_result import CollisionResult
from virtual_world.organisms.direction import Direction
from virtual_world.organisms.organism import Organism


class Plant(Organism):
    def action(self, direction: Direction = Direction.NONE) -> None:
        if random.random() < Config.PLANT_SPREAD_CHANCE:
            new_position = self._world.get_random_adjacent_position(
                self._position, empty=True
            )
            if self._world.is_position_in_world(new_position):
                self._world.add_entity(self.__class__(new_position))

    def collision(self, other: Organism, is_attacked: bool = False) -> CollisionResult:
        return CollisionResult.DEFEAT
