import random

from virtual_world.config import Config
from virtual_world.organisms.collision_result import CollisionResult
from virtual_world.organisms.direction import DirectionSquare, DirectionHexagon
from virtual_world.organisms.organism import Organism
from typing import Optional


class Plant(Organism):
    _initiative = Config.PLANT_INITIATIVE

    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        if random.random() < Config.PLANT_SPREAD_CHANCE:
            new_position = self._world.get_random_adjacent_position(
                self._position, empty=True
            )
            if self._world.is_position_in_world(new_position):
                self._world.add_entity(self.__class__(new_position))

    def collision(self, other: Organism, is_attacked: bool = False) -> CollisionResult:
        return CollisionResult.DEFEAT


class Grass(Plant):
    _strength = Config.GRASS_STRENGTH
    _color = Config.GRASS_COLOR


class Dandelion(Plant):
    _strength = Config.DANDELION_STRENGTH
    _color = Config.DANDELION_COLOR

    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        for _ in range(Config.DANDELION_SPREAD_TRIES):
            super().action(direction)


class Guarana(Plant):
    _strength = Config.GUARANA_STRENGTH
    _color = Config.GUARANA_COLOR

    def collision(self, other: Organism, is_attacked: bool = False) -> CollisionResult:
        other.increase_strength(Config.GUARANA_STRENGTH_BOOST)
        return super().collision(other, is_attacked)


class Belladonna(Plant):
    _strength = Config.BELLADONNA_STRENGTH
    _color = Config.BELLADONNA_COLOR

    def collision(self, other: Organism, is_attacked: bool = False) -> CollisionResult:
        other.die()
        return super().collision(other, is_attacked)


class HeracleumSosnowskyi(Plant):
    _strength = Config.HERACLEUM_SOSNOWSKYI_STRENGTH
    _color = Config.HERACLEUM_SOSNOWSKYI_COLOR

    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        self.kill_adjacent()
        super().action(direction)

    def kill_adjacent(self) -> None:
        from virtual_world.organisms.animals.animals import Animal, CyberSheep

        directions = self.get_possible_directions()
        for direction in directions:
            adjacent_position = self._world.get_position_in_direction(
                self.get_position(), direction
            )
            organism = self._world.get_entity(adjacent_position)
            if isinstance(organism, Animal) and not isinstance(organism, CyberSheep):
                organism.die()

    def collision(self, other: Organism, is_attacked: bool = False) -> CollisionResult:
        from virtual_world.organisms.animals.animals import Animal, CyberSheep

        if isinstance(other, Animal) and not isinstance(other, CyberSheep):
            other.die()
        return super().collision(other, is_attacked)
