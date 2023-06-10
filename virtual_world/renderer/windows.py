# mypy: ignore-errors
import re

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QRect, QPointF
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QHBoxLayout,
    QGridLayout,
    QVBoxLayout,
    QLineEdit,
    QFileDialog,
)
import virtual_world.organisms.organism as organism_module
import virtual_world.organisms.animals.animals as animals_module
import virtual_world.organisms.plants.plants as plants_module
import virtual_world.world as world_module
from virtual_world.config import Config
from virtual_world.organisms.direction import DirectionSquare, DirectionHexagon
from virtual_world.organisms.position import PositionSquare


class MainWindow(QWidget):  # type: ignore
    _world: "world_module.World"

    def __init__(
        self, world: "world_module.World", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = self._create_layout(world)
        self.setLayout(layout)
        self.setWindowTitle("Virtual World - Jerzy Szyjut 193064")
        self._world = world
        self.show()
        self.showMaximized()

    @staticmethod
    def _create_layout(world: "world_module.World") -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.addWidget(WorldWidget(world))
        side_layout = QVBoxLayout()
        legend_label = QLabel("Legend:")
        legend_label.setFixedHeight(50)
        side_layout.addWidget(legend_label)
        side_layout.addWidget(LegendWidget(world))
        logs_label = QLabel("Logs:")
        logs_label.setFixedHeight(50)
        side_layout.addWidget(logs_label)
        side_layout.addWidget(LogsWidget(world))
        layout.addLayout(side_layout)
        return layout

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        elif a0.key() == QtCore.Qt.Key.Key_Enter:
            self._world.next_turn()
            self.update()
        elif a0.key() == QtCore.Qt.Key.Key_Space:
            self._world.use_player_ability()
            self.update()
        elif a0.key() in self.get_possible_keys():
            if self._world.get_type() == world_module.World.WorldType.SQUARE:
                direction = DirectionSquare(a0.key())
            elif self._world.get_type() == world_module.World.WorldType.HEXAGONAL:
                direction = DirectionHexagon(a0.key())  # type: ignore # assignment
            else:
                raise ValueError("Invalid world type")
            self._world.move_player(direction)
            self._world.next_turn()
            self.update()
        elif a0.key() == QtCore.Qt.Key.Key_S:
            filename = get_save_file_name() + ".json"
            if filename:
                self._world.save(filename)
        elif a0.key() == QtCore.Qt.Key.Key_L:
            filename = get_load_file_name()
            if filename:
                self._world.load(filename)
                self.update()

    def get_possible_keys(self) -> list[int]:
        if self._world.get_type() == world_module.World.WorldType.SQUARE:
            return [
                direction.value
                for direction in DirectionSquare
                if direction != DirectionSquare.NONE
            ]
        elif self._world.get_type() == world_module.World.WorldType.HEXAGONAL:
            return [
                direction.value
                for direction in DirectionHexagon
                if direction != DirectionHexagon.NONE
            ]
        else:
            raise ValueError("Invalid world type")


class LogsWidget(QWidget):  # type: ignore
    _world: "world_module.World"
    _last_turn: int

    def __init__(
        self, world: "world_module.World", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setSizeIncrement(200, 200)
        self.show()
        self._world = world
        self._last_turn = world.get_turn()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QtGui.QFont("Arial", 10))
        for i, log in enumerate(self._world.get_logs()):
            painter.drawText(QPointF(0, i * 20 + 20), log)
        if self._last_turn != self._world.get_turn():
            self._last_turn = self._world.get_turn()
            self._world.clear_logs()


class LegendWidget(QWidget):  # type: ignore
    unit_size: tuple[int, int] = (Config.BASE_FIELD_SIZE, Config.BASE_FIELD_SIZE)
    _world: "world_module.World"

    def __init__(
        self, world: "world_module.World", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setFixedHeight(250)
        self._world = world
        self.show()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        for i, organism_class in enumerate(self.get_organisms()):
            self._paint_organism(i, organism_class)
        self._paint_possible_moves()
        self.paint_current_turn()

    def paint_current_turn(self) -> None:
        painter = QPainter(self)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QtGui.QFont("Arial", 10))
        painter.drawText(QPointF(100, 20), f"Current turn: {self._world.get_turn()}")
        player = self._world.get_player()
        painter.drawText(QPointF(100, 40), f"Current player ability cooldown: {player.get_special_ability_cooldown()}")  # type: ignore
        painter.drawText(QPointF(100, 60), f"Current player ability duration: {player.get_special_ability_duration()}")  # type: ignore
        painter.drawText(QPointF(100, 80), f"Current player ability active: {player.get_special_ability_active()}")  # type: ignore

    def _paint_possible_moves(self) -> None:
        moves = [
            "ESC - exit",
            "ENTER - next turn",
            "SPACE - use player ability",
            "S - save game",
            "L - load game",
        ]

        if self._world.get_type() == world_module.World.WorldType.SQUARE:
            moves += [
                "ARROW UP - move up",
                "ARROW DOWN - move down",
                "ARROW LEFT - move left",
                "ARROW RIGHT - move right",
            ]
        elif self._world.get_type() == world_module.World.WorldType.HEXAGONAL:
            moves += [
                "W - move up-left",
                "E - move up-right",
                "A - move left",
                "D - move right",
                "Z - move down-left",
                "X - move down-right",
            ]
        else:
            raise ValueError("Invalid world type")

        for i, move in enumerate(moves):
            self._paint_move(i, move)

    def _paint_move(self, i: int, move: str) -> None:
        painter = QPainter(self)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QtGui.QFont("Arial", 10))
        painter.drawText(QPointF(200, i * 20 + 100), move)

    def _paint_organism(
        self, i: int, organism_class: type["organism_module.Organism"]
    ) -> None:
        organism_object = organism_class()
        painter = QPainter(self)
        painter.setBrush(QColor(*organism_object.get_color()))
        painter.drawRect(
            QRect(0, i * self.unit_size[1], self.unit_size[0], self.unit_size[1])
        )
        painter.drawText(
            QPointF(self.unit_size[0] + 5, (i + 1) * self.unit_size[1] - 5),
            self.pascal_case_to_normal_case(organism_object.__class__.__name__),
        )

    @staticmethod
    def get_organisms() -> (
        list[type["animals_module.Animal"] | type["plants_module.Plant"]]
    ):
        from virtual_world.organisms.animals import animals
        from virtual_world.organisms.plants import plants

        return animals.Animal.__subclasses__() + plants.Plant.__subclasses__()

    @staticmethod
    def pascal_case_to_normal_case(string: str) -> str:
        words = re.findall("[A-Z][a-z]*", string)
        normal_string = " ".join(word.lower() for word in words)
        normal_string = normal_string.capitalize()
        return normal_string


class WorldWidget(QWidget):  # type: ignore
    unit_size: tuple[int, int]
    _world: "world_module.World"

    def __init__(
        self, world: "world_module.World", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setSizeIncrement(500, 500)
        self.setFixedWidth(510)
        self.setFixedHeight(510)
        self._world = world
        self.unit_size = get_unit_size(self, world.get_width(), world.get_height())
        self.show()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        for organism_object in self._world.get_entities():
            paint_organism(self, organism_object)
        self.paint_field_borders()

    def paint_field_borders(self) -> None:
        painter = QPainter(self)
        for i in range(0, self._world.get_height()):
            for j in range(0, self._world.get_width()):
                rectangle = QRect(
                    i * self.unit_size[0],
                    j * self.unit_size[1],
                    self.unit_size[0],
                    self.unit_size[1],
                )
                painter.drawRect(rectangle)


def paint_organism(
    self: WorldWidget | LegendWidget, organism_object: "organism_module.Organism"
) -> None:
    painter = QPainter(self)
    position = organism_object.get_position()
    if isinstance(position, PositionSquare):
        rectangle = QRect(
            position.get_x() * self.unit_size[0],
            position.get_y() * self.unit_size[1],
            self.unit_size[0],
            self.unit_size[1],
        )
        painter.fillRect(rectangle, QColor(*organism_object.get_color()))


def get_unit_size(
    self: QWidget, world_width: int, world_height: int
) -> tuple[int, int]:
    return self.width() // world_width, self.height() // world_height


def get_save_file_name() -> str:
    return QFileDialog.getSaveFileName(None, "Save game", "", "Text files (*.json)")[0]


def get_load_file_name() -> str:
    return QFileDialog.getOpenFileName(None, "Load game", "", "Text files (*.json)")[0]
