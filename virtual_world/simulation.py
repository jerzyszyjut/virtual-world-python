from virtual_world.renderer.application import Application
from virtual_world.world import World


class Simulation:
    def __init__(self) -> None:
        self.world = World()
        self.renderer = Application(self.world)

    def run(self) -> None:
        self.renderer.run()
