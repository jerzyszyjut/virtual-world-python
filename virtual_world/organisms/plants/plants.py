import random

from virtual_world.config import Config
from virtual_world.organisms.animals.animals import Animal, CyberSheep
from virtual_world.organisms.collision_result import CollisionResult
from virtual_world.organisms.direction import DirectionSquare, DirectionHexagon
from virtual_world.organisms.organism import Organism


class Plant(Organism):
    _initiative = Config.PLANT_INITIATIVE

    def action(self, direction: DirectionSquare | DirectionHexagon) -> None:
        if random.random() < Config.PLANT_SPREAD_CHANCE:
            new_position = self._world.get_random_adjacent_position(
                self._position, empty=True
            )
            if self._world.is_position_in_world(new_position):
                self._world.add_entity(self.__class__(new_position))

    def collision(self, other: Organism, is_attacked: bool = False) -> CollisionResult:
        return CollisionResult.DEFEAT


class HeracleumSosnowskyi(Plant):
    _strength = Config.HERACLEUM_SOSNOWSKYI_STRENGTH
    _color = Config.HERACLEUM_SOSNOWSKYI_COLOR

    def action(self, direction: DirectionSquare | DirectionHexagon) -> None:
        self.kill_adjacent()
        super().action(direction)

    def kill_adjacent(self) -> None:
        directions = self.get_possible_directions()
        for direction in directions:
            adjacent_position = self._world.get_position_in_direction(
                self.get_position(), direction
            )
            organism = self._world.get_entity(adjacent_position)
            if isinstance(organism, Animal) and not isinstance(organism, CyberSheep):
                organism.die()

    def collision(self, other: Organism, is_attacked: bool = False) -> CollisionResult:
        if isinstance(other, Animal) and not isinstance(other, CyberSheep):
            other.die()
        return super().collision(other, is_attacked)
