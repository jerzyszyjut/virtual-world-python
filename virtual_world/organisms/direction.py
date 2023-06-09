from enum import Enum

from PyQt6 import QtCore


class Direction(Enum):
    NONE = None


class DirectionSquare(Direction):  # type: ignore # misc
    UP = QtCore.Qt.Key.Key_Up
    DOWN = QtCore.Qt.Key.Key_Down
    RIGHT = QtCore.Qt.Key.Key_Right
    LEFT = QtCore.Qt.Key.Key_Left


class DirectionHexagon(Direction):  # type: ignore # misc
    LEFT = QtCore.Qt.Key.Key_A
    RIGHT = QtCore.Qt.Key.Key_D
    UP_LEFT = QtCore.Qt.Key.Key_W
    UP_RIGHT = QtCore.Qt.Key.Key_E
    DOWN_LEFT = QtCore.Qt.Key.Key_Z
    DOWN_RIGHT = QtCore.Qt.Key.Key_X
