from virtual_world.organisms.collision_result import CollisionResult
from virtual_world.organisms.direction import Direction
from virtual_world.organisms.organism import Organism


class Animal(Organism):
    def action(self, direction: Direction = Direction.NONE) -> None:
        if direction == Direction.NONE:
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
        new_position = self._world.get_random_adjacent_position(self._position)
        self._world.add_entity(self.__class__(new_position))
