from virtual_world.config import Config
from virtual_world.organisms.animals.animals import Antelope, Wolf
from virtual_world.organisms.position import PositionSquare
from virtual_world.simulation import Simulation
from virtual_world.world import World

if __name__ == "__main__":
    # simulation = Simulation()
    # simulation.run()

    world = World()
    world.add_entity(Antelope(PositionSquare(1, 0)))
    world.add_entity(Wolf(PositionSquare(0, 1)))
    world.save(Config.SAVE_FILE_NAME)

    world2 = World()
    world2.load(Config.SAVE_FILE_NAME)
    print("world2")
