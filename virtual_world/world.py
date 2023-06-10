import json
import random
from enum import Enum
from typing import Optional, Type

import virtual_world
from virtual_world.config import Config
from virtual_world.organisms.direction import (
    DirectionSquare,
    DirectionHexagon,
)
from virtual_world.organisms.factory import OrganismFactory
from virtual_world.organisms.position import PositionSquare, PositionHexagon


class World:
    import virtual_world.organisms.organism as organism

    class WorldType(Enum):
        SQUARE = 0
        HEXAGONAL = 1

    __entities: list["organism.Organism"]
    __logs: list[str]
    __turn: int
    __width: int
    __height: int
    __type: WorldType
    __player: Optional["virtual_world.organisms.animals.animals.Human"] = None

    def __init__(
        self,
        width: int = Config.WORLD_WIDTH,
        height: int = Config.WORLD_HEIGHT,
        world_type: WorldType = WorldType.SQUARE,
    ) -> None:
        from virtual_world.organisms.animals.animals import Human

        self.__entities = []
        self.__logs = []
        self.__turn = 0
        self.__width = width
        self.__height = height
        self.__type = world_type
        self.__player = Human(PositionSquare(*Config.HUMAN_DEFAULT_POSITION))
        self.add_entity(self.__player)

    def add_entity(self, entity: "organism.Organism") -> None:
        if (
            not self.get_entity(entity.get_position())
            and entity.is_alive()
            and (self.is_position_in_world(entity.get_position()))
        ):
            entity.set_world(self)
            self.__entities.append(entity)

    def remove_entity(self, entity: "organism.Organism") -> None:
        self.__entities.remove(entity)

    def get_entity(
        self, position: PositionSquare | PositionHexagon
    ) -> Optional["organism.Organism"]:
        for entity in self.__entities:
            if entity.get_position() == position:
                return entity
        return None

    def next_turn(self) -> None:
        from virtual_world.organisms.animals.animals import Human

        __entities_copy = self.__entities.copy()
        __entities_copy.sort(
            key=lambda entity_in_loop: (
                entity_in_loop.get_initiative(),
                entity_in_loop.get_age(),
            ),
            reverse=True,
        )
        for entity in __entities_copy:
            if entity.is_alive() and not isinstance(entity, Human):
                entity.action()
            entity.increase_age()

        self.remove_dead_entities()
        self.__turn += 1

    def get_random_direction(self) -> DirectionSquare | DirectionHexagon:
        if self.__type == World.WorldType.SQUARE:
            return random.choice(list(DirectionSquare))
        elif self.__type == World.WorldType.HEXAGONAL:
            return random.choice(list(DirectionHexagon))
        else:
            raise NotImplementedError

    def remove_dead_entities(self) -> None:
        self.__entities = [entity for entity in self.__entities if entity.is_alive()]

    def get_position_in_direction(
        self,
        position: PositionSquare | PositionHexagon,
        direction: DirectionSquare | DirectionHexagon,
    ) -> PositionSquare | PositionHexagon:
        if self.__type == World.WorldType.SQUARE and isinstance(
            position, PositionSquare
        ):
            if direction == DirectionSquare.UP:
                return PositionSquare(position.get_x(), position.get_y() - 1)
            elif direction == DirectionSquare.DOWN:
                return PositionSquare(position.get_x(), position.get_y() + 1)
            elif direction == DirectionSquare.LEFT:
                return PositionSquare(position.get_x() - 1, position.get_y())
            elif direction == DirectionSquare.RIGHT:
                return PositionSquare(position.get_x() + 1, position.get_y())
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    def is_position_in_world(self, position: PositionSquare | PositionHexagon) -> bool:
        if self.__type == World.WorldType.SQUARE and isinstance(
            position, PositionSquare
        ):
            return (
                0 <= position.get_x() < self.__width
                and 0 <= position.get_y() < self.__height
            )
        else:
            raise NotImplementedError

    def get_organism_at_position(
        self, position: PositionSquare | PositionHexagon
    ) -> Optional["organism.Organism"]:
        for entity in self.__entities:
            if entity.is_alive() and entity.get_position() == position:
                return entity
        return None

    def move_organism(
        self, organism: "organism.Organism", position: PositionSquare | PositionHexagon
    ) -> None:
        if self.is_position_in_world(position):
            organism.set_position(position)

    def get_random_adjacent_position(
        self, position: PositionSquare | PositionHexagon, empty: bool = False
    ) -> PositionSquare | PositionHexagon:
        if self.__type == World.WorldType.SQUARE and isinstance(
            position, PositionSquare
        ):
            choices = [
                PositionSquare(position.get_x(), position.get_y() - 1),
                PositionSquare(position.get_x(), position.get_y() + 1),
                PositionSquare(position.get_x() - 1, position.get_y()),
                PositionSquare(position.get_x() + 1, position.get_y()),
            ]

            if empty:
                choices = [
                    choice
                    for choice in choices
                    if self.get_organism_at_position(choice) is None
                ]

            return random.choice(choices)
        else:
            raise NotImplementedError

    def get_all_neighbours(
        self, position: PositionSquare | PositionHexagon
    ) -> list["organism.Organism"]:
        if self.__type == World.WorldType.SQUARE and isinstance(
            position, PositionSquare
        ):
            neighbours = []
            for direction in DirectionSquare:
                if direction == DirectionSquare.NONE:
                    continue
                neighbour = self.get_organism_at_position(
                    self.get_position_in_direction(position, direction)
                )
                if neighbour is not None:
                    neighbours.append(neighbour)
            return neighbours
        else:
            raise NotImplementedError

    def get_closest_organism_of_type(
        self,
        position: PositionSquare | PositionHexagon,
        organism_type: Type["organism.Organism"],
    ) -> Optional["organism.Organism"]:
        if self.__type == World.WorldType.SQUARE and isinstance(
            position, PositionSquare
        ):
            closest = None
            closest_distance = None
            for entity in self.__entities:
                if isinstance(entity, organism_type):
                    entity_position = entity.get_position()
                    if isinstance(entity_position, PositionSquare):
                        distance = position.get_distance(entity_position)
                        if closest is None or distance < closest_distance:
                            closest = entity
                            closest_distance = distance
            return closest
        else:
            raise NotImplementedError

    def get_direction_to_position(
        self,
        position: PositionSquare | PositionHexagon,
        target_position: PositionSquare | PositionHexagon,
    ) -> DirectionSquare | DirectionHexagon:
        if (
            self.__type == World.WorldType.SQUARE
            and isinstance(position, PositionSquare)
            and isinstance(target_position, PositionSquare)
        ):
            if position.get_x() < target_position.get_x():
                return DirectionSquare.RIGHT
            elif position.get_x() > target_position.get_x():
                return DirectionSquare.LEFT
            elif position.get_y() < target_position.get_y():
                return DirectionSquare.DOWN
            elif position.get_y() > target_position.get_y():
                return DirectionSquare.UP
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    def move_player(self, direction: DirectionSquare | DirectionHexagon) -> None:
        if self.__player is not None:
            self.__player.action(direction)

    def use_player_ability(self) -> None:
        if self.__player is not None:
            self.__player.use_special_ability()

    def get_player(self) -> Optional["virtual_world.organisms.animals.animals.Human"]:
        return self.__player

    def __dict__(self) -> dict:  # type: ignore # override
        from virtual_world.organisms.animals.animals import Human

        return {
            "turn": self.__turn,
            "width": self.__width,
            "height": self.__height,
            "player": self.__player.__dict__() if self.__player is not None else None,
            "entities": [
                entity.__dict__()
                for entity in self.__entities
                if not isinstance(entity, Human)
            ],
        }

    def save(self, path: str) -> None:
        with open(path, "w+") as file:
            json.dump(self.__dict__(), file)

    def load(self, path: str) -> None:
        from virtual_world.organisms.animals.animals import Human

        with open(path, "r") as file:
            data = json.load(file)
            self.__turn = data["turn"]
            self.__width = data["width"]
            self.__height = data["height"]
            self.__entities = []
            if data["player"] is not None:
                self.__player = Human()
                self.__player.set_from_dict(data["player"])
                self.add_entity(self.__player)
            else:
                self.__player = None
            for entity_data in data["entities"]:
                entity = OrganismFactory.create(entity_data)
                self.add_entity(entity)

    def get_logs(self) -> list[str]:
        return self.__logs

    def add_log(self, log: str) -> None:
        self.__logs.append(log)

    def clear_logs(self) -> None:
        self.__logs = []

    def get_turn(self) -> int:
        return self.__turn

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def get_entities(self) -> list["organism.Organism"]:
        return self.__entities

    def get_type(self) -> WorldType:
        return self.__type

    def set_type(self, world_type: WorldType) -> None:
        self.__type = world_type
