from enum import Enum


class CollisionResult(Enum):
    VICTORY = (0,)
    DEFEAT = (1,)
    TIE = (2,)
    ESCAPE = 3
