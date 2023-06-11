# mypy: ignore-errors
import re
from typing import Tuple, Optional

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QRect, QPointF
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QLineEdit,
    QComboBox,
    QPushButton,
)
from PyQt6.QtWidgets import QDialog

import virtual_world.organisms.animals.animals as animals_module
import virtual_world.organisms.organism as organism_module
import virtual_world.organisms.plants.plants as plants_module
import virtual_world.world as world_module
from virtual_world.config import Config
from virtual_world.organisms.direction import DirectionSquare, DirectionHexagon
from virtual_world.organisms.factory import OrganismFactory
from virtual_world.organisms.position import PositionSquare, PositionHexagon


class MainWindow(QWidget):  # type: ignore
    _world: Optional["world_module.World"] = None

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Virtual World - Jerzy Szyjut 193064")
        WorldDialog(parent=self)
        self.show()
        self.showMaximized()

    def create_layout(self) -> None:
        layout = QHBoxLayout()
        layout.addWidget(WorldWidget(self._world))
        side_layout = QVBoxLayout()
        legend_label = QLabel("Legend:")
        legend_label.setFixedHeight(50)
        side_layout.addWidget(legend_label)
        side_layout.addWidget(LegendWidget(self._world))
        logs_label = QLabel("Logs:")
        logs_label.setFixedHeight(50)
        side_layout.addWidget(logs_label)
        side_layout.addWidget(LogsWidget(self._world))
        layout.addLayout(side_layout)
        self.setLayout(layout)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if self._world is None:
            return
        if a0.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        elif a0.key() == QtCore.Qt.Key.Key_Return:
            self.__go_to_next_turn()
        elif a0.key() == QtCore.Qt.Key.Key_Space:
            self.__use_player_ability()
        elif a0.key() in self.get_possible_keys():
            self.__move_player(a0.key())
        elif a0.key() == QtCore.Qt.Key.Key_S:
            self.__save()
        elif a0.key() == QtCore.Qt.Key.Key_L:
            self.__load()

    def __go_to_next_turn(self) -> None:
        if self._world.get_type() == self._world.WorldType.SQUARE:
            self._world.next_turn(DirectionSquare.NONE)
        elif self._world.get_type() == self._world.WorldType.HEXAGONAL:
            self._world.next_turn(DirectionHexagon.NONE)
        else:
            raise ValueError("Invalid world type")
        self.update()

    def __use_player_ability(self) -> None:
        self._world.use_player_ability()
        self.update()

    def __move_player(self, key: int) -> None:
        if self._world.get_type() == world_module.World.WorldType.SQUARE:
            direction = DirectionSquare(key)
        elif self._world.get_type() == world_module.World.WorldType.HEXAGONAL:
            direction = DirectionHexagon(key)  # type: ignore # assignment
        else:
            raise ValueError("Invalid world type")
        self._world.next_turn(direction)
        self.update()

    def __save(self) -> None:
        filename = self.__get_save_file_name()
        if ".json" not in filename:
            filename += ".json"
        if filename:
            self._world.save(filename)

    def __load(self) -> None:
        filename = self.__get_load_file_name()
        if filename:
            self._world.load(filename)
            self.update()

    @staticmethod
    def __get_save_file_name() -> str:
        return QFileDialog.getSaveFileName(
            None, "Save game", "", "Text files (*.json)"
        )[0]

    @staticmethod
    def __get_load_file_name() -> str:
        return QFileDialog.getOpenFileName(
            None, "Load game", "", "Text files (*.json)"
        )[0]

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

    def set_world(self, world: "world_module.World") -> None:
        self._world = world
        self.update()


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
        painter.drawText(
            QPointF(100, 40),
            f"Current player ability cooldown: {player.get_special_ability_cooldown()}",
        )  # type: ignore
        painter.drawText(
            QPointF(100, 60),
            f"Current player ability duration: {player.get_special_ability_duration()}",
        )  # type: ignore
        painter.drawText(
            QPointF(100, 80),
            f"Current player ability active: {player.get_special_ability_active()}",
        )  # type: ignore

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
        self.unit_size = self.__get_unit_size(world.get_width(), world.get_height())
        self.show()

    def __get_unit_size(self, world_width: int, world_height: int) -> tuple[int, int]:
        return (self.width() - 10) // world_width, (self.height() - 10) // world_height

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        for organism_object in self._world.get_entities():
            self.__paint_organism(organism_object)
        self.paint_field_borders()

    def paint_field_borders(self) -> None:
        painter = QPainter(self)
        for i in range(0, self._world.get_width()):
            for j in range(0, self._world.get_height()):
                rectangle = QRect(
                    i * self.unit_size[0],
                    j * self.unit_size[1],
                    self.unit_size[0],
                    self.unit_size[1],
                )
                painter.drawRect(rectangle)

    def __paint_organism(self, organism_object: "organism_module.Organism") -> None:
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

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        position = self.__get_position_from_mouse_position((a0.pos().x(), a0.pos().y()))
        if position is not None:
            self.__open_organism_choice_dialog(position)

    def __get_position_from_mouse_position(
        self, mouse_position: tuple[int, int]
    ) -> PositionSquare | PositionHexagon:
        if self._world.get_type() == world_module.World.WorldType.SQUARE:
            position = PositionSquare(
                mouse_position[0] // self.unit_size[0],
                mouse_position[1] // self.unit_size[1],
            )
            if self._world.is_position_in_world(position):
                return position
        else:
            raise NotImplementedError

    def __open_organism_choice_dialog(
        self, position: PositionSquare | PositionHexagon
    ) -> None:
        organism_dialog = OrganismDialog(self, position)
        organism_dialog.exec()

    def add_organism(self, organism: "organism_module.Organism") -> None:
        self._world.add_entity(organism)
        self.update()


class WorldDialog(QDialog):  # type: ignore
    def __init__(self, parent: MainWindow | None = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("World settings")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.world_width = QLineEdit()
        self.world_width.setPlaceholderText("World width")
        self.world_height = QLineEdit()
        self.world_height.setPlaceholderText("World height")
        self.world_type = QComboBox()
        self.world_type.addItems(["Square", "Hexagonal"])
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.world_width)
        self.layout.addWidget(self.world_height)
        self.layout.addWidget(self.world_type)
        self.layout.addWidget(self.submit_button)
        self.show()

    def submit(self) -> None:
        if self.world_width.text() and self.world_height.text():
            world_width = int(self.world_width.text())
            world_height = int(self.world_height.text())
            if self.world_type.currentText() == "Square":
                world = world_module.World(
                    world_width, world_height, world_module.World.WorldType.SQUARE
                )
            elif self.world_type.currentText() == "Hexagonal":
                world = world_module.World(
                    world_width, world_height, world_module.World.WorldType.HEXAGONAL
                )
            else:
                raise ValueError("Invalid world type")
            self.parent.set_world(world)
            self.parent.create_layout()
            self.close()


# Create dialog that will allow to choose organism to add to the world
class OrganismDialog(QDialog):
    def __init__(
        self, parent: QWidget, position: PositionSquare | PositionHexagon
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.position = position
        self.setWindowTitle("Choose organism")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.organism_type = QComboBox()
        self.organism_type.addItems(self.get_organisms_names())
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.organism_type)
        self.layout.addWidget(self.submit_button)
        self.show()

    def submit(self) -> None:
        if self.organism_type.currentText():
            organism_name = self.organism_type.currentText()
            organism = OrganismFactory.create_base_organism(
                organism_name, self.position
            )
            self.parent.add_organism(organism)
            self.close()

    @staticmethod
    def get_organisms_names() -> list[str]:
        from virtual_world.organisms.animals import animals
        from virtual_world.organisms.plants import plants

        subclasses = animals.Animal.__subclasses__() + plants.Plant.__subclasses__()
        return [
            subclass.__name__ for subclass in subclasses if subclass.__name__ != "Human"
        ]
