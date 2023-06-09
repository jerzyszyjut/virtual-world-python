import random
from enum import Enum
from typing import Optional

from virtual_world.config import Config
from virtual_world.organisms.direction import (
    Direction,
    DirectionSquare,
    DirectionHexagon,
)
from virtual_world.organisms.organism import Organism
from virtual_world.organisms.position import PositionSquare, PositionHexagon


class World:
    class WorldType(Enum):
        SQUARE = 0
        HEXAGONAL = 1

    __entities: list[Organism]
    __logs: list[str]
    __turn: int
    __width: int
    __height: int
    __type: WorldType

    def __init__(
        self,
        width: int = Config.WORLD_WIDTH,
        height: int = Config.WORLD_HEIGHT,
        type: WorldType = WorldType.SQUARE,
    ) -> None:
        self.__entities = []
        self.__logs = []
        self.__turn = 0
        self.__width = width
        self.__height = height
        self.__type = type

    def add_entity(self, entity: Organism) -> None:
        self.__entities.append(entity)

    def remove_entity(self, entity: Organism) -> None:
        self.__entities.remove(entity)

    def get_entity(
        self, position: PositionSquare | PositionHexagon
    ) -> Optional[Organism]:
        for entity in self.__entities:
            if entity.get_position() == position:
                return entity
        return None

    def next_turn(self) -> None:
        self.__turn += 1
        # TODO: implement

    def get_random_direction(self) -> DirectionSquare | DirectionHexagon:
        if self.__type == World.WorldType.SQUARE:
            return random.choice(list(DirectionSquare))
        elif self.__type == World.WorldType.HEXAGONAL:
            return random.choice(list(DirectionHexagon))
        else:
            raise NotImplementedError

    def get_position_in_direction(
        self, position: PositionSquare | PositionHexagon, direction: Direction
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
    ) -> Optional[Organism]:
        for entity in self.__entities:
            if entity.get_position() == position:
                return entity
        return None

    @staticmethod
    def move_organism(
        organism: Organism, position: PositionSquare | PositionHexagon
    ) -> None:
        organism.set_position(position)

    def get_random_adjacent_position(
        self, position: PositionSquare | PositionHexagon
    ) -> PositionSquare | PositionHexagon:
        if self.__type == World.WorldType.SQUARE and isinstance(
            position, PositionSquare
        ):
            return random.choice(
                [
                    PositionSquare(position.get_x(), position.get_y() - 1),
                    PositionSquare(position.get_x(), position.get_y() + 1),
                    PositionSquare(position.get_x() - 1, position.get_y()),
                    PositionSquare(position.get_x() + 1, position.get_y()),
                ]
            )
        else:
            raise NotImplementedError

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
