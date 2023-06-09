from abc import ABC
from typing import Optional, Tuple, TypedDict

from virtual_world.organisms.collision_result import CollisionResult
from virtual_world.organisms.direction import (
    DirectionSquare,
    DirectionHexagon,
)
from virtual_world.organisms.position import PositionSquare, PositionHexagon


class Organism(ABC):
    import virtual_world.world as world

    _strength: int
    _initiative: int
    _color: Tuple[int, int, int]
    _age: int = 0
    _position: PositionSquare | PositionHexagon
    _alive: bool = True
    _world: "world.World"

    def __init__(
        self, position: PositionSquare | PositionHexagon = PositionSquare(0, 0)
    ) -> None:
        self._position = position
        self._alive = True
        self._age = 0

    def action(
        self, direction: Optional[DirectionSquare | DirectionHexagon] = None
    ) -> None:
        pass

    def collision(
        self, other: "Organism", is_attacked: bool = False
    ) -> CollisionResult:
        if not is_attacked:
            collision_result = other.collision(self, True)
            if self.is_stronger(other) and collision_result in (  # type: ignore # comparison-overlap
                collision_result.TIE,
                collision_result.ESCAPE,
            ):
                return collision_result
        if self.is_stronger(other, is_attacked):
            return CollisionResult.VICTORY
        else:
            return CollisionResult.DEFEAT

    def get_possible_directions(self) -> list[DirectionSquare | DirectionHexagon]:
        if self._position.__class__.__name__ == "PositionSquare":
            return list(filter(lambda d: d != DirectionSquare.NONE, DirectionSquare))
        elif self._position.__class__.__name__ == "PositionHexagon":
            return list(filter(lambda d: d != DirectionHexagon.NONE, DirectionHexagon))
        else:
            raise ValueError("Unknown position type")

    def is_stronger(self, other: "Organism", is_attacked: bool = True) -> bool:
        if is_attacked:
            return self._strength > other.get_strength()
        return self._strength >= other.get_strength()

    def has_higher_initiative(self, other: "Organism") -> bool:
        if self._initiative == other.get_initiative():
            return self._age > other.get_age()
        return self._initiative > other.get_initiative()

    def get_initiative(self) -> int:
        return self._initiative

    def get_strength(self) -> int:
        return self._strength

    def increase_strength(self, strength: int) -> None:
        self._strength += strength

    def get_position(self) -> PositionSquare | PositionHexagon:
        return self._position

    def set_position(self, position: PositionSquare | PositionHexagon) -> None:
        self._position = position

    def get_age(self) -> int:
        return self._age

    def increase_age(self) -> None:
        self._age += 1

    def die(self) -> None:
        self._alive = False

    def is_alive(self) -> bool:
        return self._alive

    def get_color(self) -> Tuple[int, int, int]:
        return self._color

    def set_world(self, world: "world.World") -> None:
        self._world = world

    def get_world(self) -> "world.World":
        return self._world

    class OrganismRepresentation(TypedDict):
        strength: int
        initiative: int
        age: int
        position: PositionSquare.PositionRepresentation | PositionHexagon.PositionRepresentation
        alive: bool
        color: Tuple[int, int, int]
        type: str

    def __dict__(self) -> OrganismRepresentation:  # type: ignore # override
        return {
            "strength": self._strength,
            "initiative": self._initiative,
            "age": self._age,
            "position": self._position.__dict__(),
            "alive": self._alive,
            "color": self._color,
            "type": self.__class__.__name__,
        }

    def set_from_dict(self, data: OrganismRepresentation) -> None:
        self._strength = data["strength"]
        self._initiative = data["initiative"]
        self._age = data["age"]
        if len(data["position"]) == 2:
            self._position = PositionSquare(**data["position"])
        elif len(data["position"]) == 3:
            self._position = PositionHexagon(**data["position"])
        self._alive = data["alive"]
        self._color = data["color"]

    def __str__(self) -> str:
        return self.__class__.__name__
