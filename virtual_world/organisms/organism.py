from typing import Tuple, Union, TypedDict

from virtual_world.organisms.collision_result import CollisionResult
from virtual_world.organisms.direction import Direction
from virtual_world.organisms.position import PositionSquare, PositionHexagon


class Organism:
    from virtual_world.world import World

    __strength: int
    __initiative: int
    __age: int
    __position: PositionSquare | PositionHexagon
    __alive: bool
    __world: World
    __color: Tuple[int, int, int]

    def __init__(self, position: PositionSquare | PositionHexagon) -> None:
        self.__position = position
        self.__alive = True
        self.__age = 0

    def action(self, direction: Direction = Direction.NONE) -> None:
        pass

    def collision(
        self, attacker: "Organism", is_attacked: bool = False
    ) -> CollisionResult:
        if not is_attacked:
            collision_result = attacker.collision(self, True)
            if self.is_stronger(attacker) and collision_result in (  # type: ignore # comparison-overlap
                collision_result.TIE,
                collision_result.ESCAPE,
            ):
                if collision_result == collision_result.TIE:  # type: ignore # comparison-overlap
                    self.__world.add_log(f"{self} and {attacker} tied a fight")
                elif collision_result == collision_result.ESCAPE:  # type: ignore # comparison-overlap
                    self.__world.add_log(f"{self} escaped from {attacker}")
                return collision_result
        if self.is_stronger(attacker, is_attacked):
            self.__world.add_log(
                f"{self} killed {attacker} at {attacker.get_position()}"
            )
            return CollisionResult.VICTORY
        else:
            if not is_attacked:
                self.__world.add_log(
                    f"{attacker} was killed by {self} at {self.get_position()}"
                )
            return CollisionResult.DEFEAT

    def is_stronger(self, other: "Organism", is_attacked: bool = True) -> bool:
        if is_attacked:
            return self.__strength > other.get_strength()
        return self.__strength >= other.get_strength()

    def has_higher_initiative(self, other: "Organism") -> bool:
        if self.__initiative == other.get_initiative():
            return self.__age > other.get_age()
        return self.__initiative > other.get_initiative()

    def get_initiative(self) -> int:
        return self.__initiative

    def get_strength(self) -> int:
        return self.__strength

    def increase_strength(self, strength: int) -> None:
        self.__strength += strength

    def get_position(self) -> PositionSquare | PositionHexagon:
        return self.__position

    def set_position(self, position: PositionSquare | PositionHexagon) -> None:
        self.__position = position

    def get_age(self) -> int:
        return self.__age

    def increase_age(self) -> None:
        self.__age += 1

    def die(self) -> None:
        self.__alive = False

    def is_alive(self) -> bool:
        return self.__alive

    def get_color(self) -> Tuple[int, int, int]:
        return self.__color

    def set_world(self, world: "World") -> None:
        self.__world = world

    def get_world(self) -> "World":
        return self.__world

    class OrganismRepresentation(TypedDict):
        strength: int
        initiative: int
        age: int
        position: PositionSquare | PositionHexagon
        alive: bool
        color: Tuple[int, int, int]

    def __dict__(self) -> OrganismRepresentation:  # type: ignore # override
        return {
            "strength": self.__strength,
            "initiative": self.__initiative,
            "age": self.__age,
            "position": self.__position,
            "alive": self.__alive,
            "color": self.__color,
        }

    def set_from_dict(self, data: OrganismRepresentation) -> None:
        self.__strength = data["strength"]
        self.__initiative = data["initiative"]
        self.__age = data["age"]
        self.__position = data["position"]
        self.__alive = data["alive"]
        self.__color = data["color"]
