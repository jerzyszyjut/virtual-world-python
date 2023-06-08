from enum import Enum


class CollisionResult(Enum):
    VICTORY: int = 0
    DEFEAT: int = 1
    TIE: int = 2
    ESCAPE: int = 3
