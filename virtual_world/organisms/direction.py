from enum import Enum

from PyQt6 import QtCore


class Direction(Enum):
    UP = QtCore.Qt.Key.Key_Up
    DOWN = QtCore.Qt.Key.Key_Down
    LEFT = QtCore.Qt.Key.Key_Left
    RIGHT = QtCore.Qt.Key.Key_Right
    NONE = None
