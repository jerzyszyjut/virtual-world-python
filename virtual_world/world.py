from typing import Optional

from virtual_world.config import Config
from virtual_world.organisms.organism import Organism
from virtual_world.organisms.position import Position


class World:
    __entities: list[Organism]
    __logs: list[str]
    __turn: int
    __width: int
    __height: int

    def __init__(
        self, width: int = Config.WORLD_WIDTH, height: int = Config.WORLD_HEIGHT
    ) -> None:
        self.__entities = []
        self.__logs = []
        self.__turn = 0
        self.__width = width
        self.__height = height

    def add_entity(self, entity: Organism) -> None:
        self.__entities.append(entity)

    def remove_entity(self, entity: Organism) -> None:
        self.__entities.remove(entity)

    def get_entity(self, position: Position) -> Optional[Organism]:
        for entity in self.__entities:
            if entity.get_position() == position:
                return entity
        return None

    def next_turn(self) -> None:
        self.__turn += 1
        # TODO: implement

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
