from typing import Tuple, Union, TypedDict

from virtual_world.organisms.collision_result import CollisionResult
from virtual_world.organisms.direction import Direction
from virtual_world.organisms.position import PositionSquare, PositionHexagon


class Organism:
    from virtual_world.world import World

    _strength: int
    _initiative: int
    _age: int
    _position: PositionSquare | PositionHexagon
    _alive: bool
    _world: World
    _color: Tuple[int, int, int]

    def __init__(self, position: PositionSquare | PositionHexagon) -> None:
        self._position = position
        self._alive = True
        self._age = 0

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
                    self._world.add_log(f"{self} and {attacker} tied a fight")
                elif collision_result == collision_result.ESCAPE:  # type: ignore # comparison-overlap
                    self._world.add_log(f"{self} escaped from {attacker}")
                return collision_result
        if self.is_stronger(attacker, is_attacked):
            self._world.add_log(
                f"{self} killed {attacker} at {attacker.get_position()}"
            )
            return CollisionResult.VICTORY
        else:
            if not is_attacked:
                self._world.add_log(
                    f"{attacker} was killed by {self} at {self.get_position()}"
                )
            return CollisionResult.DEFEAT

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

    def set_world(self, world: "World") -> None:
        self._world = world

    def get_world(self) -> "World":
        return self._world

    class OrganismRepresentation(TypedDict):
        strength: int
        initiative: int
        age: int
        position: PositionSquare | PositionHexagon
        alive: bool
        color: Tuple[int, int, int]

    def __dict__(self) -> OrganismRepresentation:  # type: ignore # override
        return {
            "strength": self._strength,
            "initiative": self._initiative,
            "age": self._age,
            "position": self._position,
            "alive": self._alive,
            "color": self._color,
        }

    def set_from_dict(self, data: OrganismRepresentation) -> None:
        self._strength = data["strength"]
        self._initiative = data["initiative"]
        self._age = data["age"]
        self._position = data["position"]
        self._alive = data["alive"]
        self._color = data["color"]
