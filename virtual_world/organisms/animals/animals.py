import random

from virtual_world.config import Config
from virtual_world.organisms.collision_result import CollisionResult
from virtual_world.organisms.direction import DirectionSquare, DirectionHexagon
from virtual_world.organisms.organism import Organism
from typing import Optional


class Animal(Organism):
    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        if direction is None:
            direction = self._world.get_random_direction()

        new_position = self._world.get_position_in_direction(self._position, direction)

        if self._world.is_position_in_world(new_position):
            other_organism = self._world.get_organism_at_position(new_position)

            if other_organism is None:
                self._world.move_organism(self, new_position)
            else:
                if other_organism.__class__.__name__ == self.__class__.__name__:
                    self.reproduce(other_organism)
                else:
                    collision_result = self.collision(other_organism)
                    if collision_result == CollisionResult.VICTORY:
                        self._world.move_organism(self, new_position)
                        other_organism.die()
                    elif collision_result == CollisionResult.DEFEAT:
                        self.die()
                    elif collision_result == CollisionResult.ESCAPE:
                        self._world.move_organism(self, new_position)

    def reproduce(self, other: "Organism") -> None:
        self._world.add_log(f"{self} reproduced with {other}")
        new_position = self._world.get_random_adjacent_position(
            self._position, empty=True
        )
        self._world.add_entity(self.__class__(new_position))


class Sheep(Animal):
    _strength = Config.SHEEP_STRENGTH
    _initiative = Config.SHEEP_INITIATIVE
    _color = Config.SHEEP_COLOR


class Wolf(Animal):
    _strength = Config.WOLF_STRENGTH
    _initiative = Config.WOLF_INITIATIVE
    _color = Config.WOLF_COLOR


class Turtle(Animal):
    _strength = Config.TURTLE_STRENGTH
    _initiative = Config.TURTLE_INITIATIVE
    _color = Config.TURTLE_COLOR

    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        if random.random() < Config.TURTLE_MOVE_CHANCE:
            super().action(direction)
        self._world.add_log(f"{self} is too lazy to move")

    def collision(self, other: Organism, is_attacked: bool = False) -> CollisionResult:
        if (
            other.__class__.__name__ != "Turtle"
            and other.get_strength() < Config.TURTLE_REFLECTION_STRENGTH
        ):
            self._world.add_log(f"{self} reflected attack from {other}")
            return CollisionResult.TIE
        return super().collision(other, is_attacked)


class Fox(Animal):
    _strength = Config.FOX_STRENGTH
    _initiative = Config.FOX_INITIATIVE
    _color = Config.FOX_COLOR

    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        possible_directions = self.get_possible_directions()
        if isinstance(direction, DirectionSquare):
            possible_directions.remove(DirectionSquare.NONE)
        elif isinstance(direction, DirectionHexagon):
            possible_directions.remove(DirectionHexagon.NONE)

        possible_directions = list(
            filter(
                lambda d: self._world.get_entity(self._position) is None,
                possible_directions,
            )
        )

        if len(possible_directions) == 0:
            self._world.add_log(f"There is no place for {self} to move")
        else:
            super().action(random.choice(possible_directions))


class Human(Animal):
    _strength = Config.HUMAN_STRENGTH
    _initiative = Config.HUMAN_INITIATIVE
    _color = Config.HUMAN_COLOR
    _special_ability_cooldown = 0
    _special_ability_duration = 0
    _special_ability_active = False

    def use_special_ability(self) -> None:
        self._special_ability_cooldown = Config.HUMAN_ABILITY_COOLDOWN
        self._special_ability_duration = Config.HUMAN_ABILITY_DURATION
        self._special_ability_active = True
        self._world.add_log(f"{self} used special ability")

    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        self.perform_special_ability()

        if self._special_ability_active:
            self._special_ability_duration -= 1
            if self._special_ability_duration == 0:
                self._special_ability_active = False
                self._world.add_log(f"{self} special ability ended")
        else:
            self._special_ability_cooldown -= 1
            if self._special_ability_cooldown == 0:
                self._world.add_log(f"{self} special ability is ready")

        super().action(direction)

    def perform_special_ability(self) -> None:
        if self._special_ability_active:
            neighbors = self._world.get_all_neighbours(self._position)
            for neighbor in neighbors:
                neighbor.die()
                self._world.add_log(f"{self} killed {neighbor} with special ability")

    def get_special_ability_cooldown(self) -> int:
        return self._special_ability_cooldown

    def get_special_ability_duration(self) -> int:
        return self._special_ability_duration

    def get_special_ability_active(self) -> bool:
        return self._special_ability_active


class Antelope(Animal):
    _strength = Config.ANTELOPE_STRENGTH
    _initiative = Config.ANTELOPE_INITIATIVE
    _color = Config.ANTELOPE_COLOR

    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        for i in range(Config.ANTELOPE_MOVE_RANGE):
            super().action(direction)

    def collision(self, other: Organism, is_attacked: bool = False) -> CollisionResult:
        escape_position = self._world.get_random_adjacent_position(
            self._position, empty=True
        )
        if escape_position is None:
            return super().collision(other, is_attacked)

        if random.random() < Config.ANTELOPE_ESCAPE_CHANCE:
            self._world.add_log(f"{self} escaped from {other}")
            self._world.move_organism(self, escape_position)
            return CollisionResult.ESCAPE

        return super().collision(other, is_attacked)


class CyberSheep(Animal):
    _strength = Config.CYBER_SHEEP_STRENGTH
    _initiative = Config.CYBER_SHEEP_INITIATIVE
    _color = Config.CYBER_SHEEP_COLOR

    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        from virtual_world.organisms.plants.plants import HeracleumSosnowskyi

        closest_heracleum_sosnowskyi = self._world.get_closest_organism_of_type(
            self.get_position(), HeracleumSosnowskyi
        )
        if closest_heracleum_sosnowskyi is None:
            super().action(direction)
        else:
            self._world.add_log(f"{self} is going to {closest_heracleum_sosnowskyi}")
            direction = self._world.get_direction_to_position(
                self._position, closest_heracleum_sosnowskyi.get_position()
            )
            super().action(direction)

    def collision(
        self, other: "Organism", is_attacked: bool = False
    ) -> CollisionResult:
        from virtual_world.organisms.plants.plants import HeracleumSosnowskyi

        if isinstance(other, HeracleumSosnowskyi):
            self._world.add_log(f"{self} ate {other}")
            other.die()
            return CollisionResult.VICTORY
        return super().collision(other, is_attacked)
