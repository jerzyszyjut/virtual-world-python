from virtual_world.renderer.application import Application


class Simulation:
    def __init__(self) -> None:
        self.renderer = Application()

    def run(self) -> None:
        self.renderer.run()
