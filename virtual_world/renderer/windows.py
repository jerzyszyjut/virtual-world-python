import re

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QRect, QPointF
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout
import virtual_world.organisms.organism as organism_module
import virtual_world.organisms.animals.animals as animals_module
import virtual_world.organisms.plants.plants as plants_module
import virtual_world.world as world_module
from virtual_world.config import Config
from virtual_world.organisms.position import PositionSquare


class MainWindow(QWidget):
    def __init__(
        self, world: "world_module.World", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = self._create_layout(world)
        self.setLayout(layout)
        self.setWindowTitle("Virtual World - Jerzy Szyjut 193064")
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
        side_layout.addWidget(LegendWidget())
        logs_label = QLabel("Logs:")
        logs_label.setFixedHeight(50)
        side_layout.addWidget(logs_label)
        side_layout.addWidget(LogsWidget(world))
        layout.addLayout(side_layout)
        return layout


class LogsWidget(QWidget):
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


class LegendWidget(QWidget):
    unit_size: tuple[int, int] = (Config.BASE_FIELD_SIZE, Config.BASE_FIELD_SIZE)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setFixedHeight(250)
        self.show()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        for i, organism_class in enumerate(self.get_organisms()):
            self._paint_organism(i, organism_class)

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


class WorldWidget(QWidget):
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
