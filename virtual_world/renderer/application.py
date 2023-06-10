from PyQt6.QtWidgets import QApplication

from virtual_world.renderer.windows import MainWindow, WorldDialog
from virtual_world.world import World


class Application:
    def __init__(self) -> None:
        self._app = QApplication([])
        self._window = MainWindow()

    def run(self) -> None:
        self._window.show()
        self._app.exec()
