from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QGridLayout


class MainWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = self._create_layout()
        self.setLayout(layout)
        self.setWindowTitle("Virtual World - Jerzy Szyjut 193064")
        self.setSizeIncrement(800, 600)
        self.setStyleSheet("background-color: #ffffff; color: #000000;")

    @staticmethod
    def _create_layout() -> QGridLayout:
        layout = QGridLayout()
        layout.addWidget(WorldWidget(), 0, 0, 1, 0)
        layout.addWidget(LegendWidget(), 0, 1)
        layout.addWidget(LogsWidget(), 1, 1)
        return layout


class LogsWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Logs"))
        self.setLayout(layout)


class LegendWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Legend"))
        self.setLayout(layout)


class WorldWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.addWidget(QLabel("World"))
        self.setLayout(layout)
