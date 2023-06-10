from enum import Enum

from PyQt6 import QtCore


class DirectionSquare(Enum):
    UP = QtCore.Qt.Key.Key_Up
    DOWN = QtCore.Qt.Key.Key_Down
    RIGHT = QtCore.Qt.Key.Key_Right
    LEFT = QtCore.Qt.Key.Key_Left
    NONE = None


class DirectionHexagon(Enum):
    LEFT = QtCore.Qt.Key.Key_A
    RIGHT = QtCore.Qt.Key.Key_D
    UP_LEFT = QtCore.Qt.Key.Key_W
    UP_RIGHT = QtCore.Qt.Key.Key_E
    DOWN_LEFT = QtCore.Qt.Key.Key_Z
    DOWN_RIGHT = QtCore.Qt.Key.Key_X
    NONE = None
