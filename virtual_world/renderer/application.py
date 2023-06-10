from PyQt6.QtWidgets import QApplication

from virtual_world.renderer.windows import MainWindow
from virtual_world.world import World


class Application:
    def __init__(self, world: World) -> None:
        self._app = QApplication([])
        self._window = MainWindow(world)

    def run(self) -> None:
        self._window.show()
        self._app.exec()
