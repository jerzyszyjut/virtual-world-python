from typing import Tuple


class Config:
    WORLD_WIDTH: int = 20
    WORLD_HEIGHT: int = 20

    HUMAN_STRENGTH: int = 5
    HUMAN_INITIATIVE: int = 4
    HUMAN_COLOR: Tuple[int, int, int] = (0, 0, 0)
    WOLF_STRENGTH: int = 9
    WOLF_INITIATIVE: int = 5
    WOLF_COLOR: Tuple[int, int, int] = (255, 0, 0)
    SHEEP_STRENGTH: int = 4
    SHEEP_INITIATIVE: int = 4
    SHEEP_COLOR: Tuple[int, int, int] = (0, 255, 0)
    FOX_STRENGTH: int = 3
    FOX_INITIATIVE: int = 7
    FOX_COLOR: Tuple[int, int, int] = (0, 0, 255)
    TURTLE_STRENGTH: int = 2
    TURTLE_INITIATIVE: int = 1
    TURTLE_COLOR: Tuple[int, int, int] = (255, 255, 0)
    ANTELOPE_STRENGTH: int = 4
    ANTELOPE_INITIATIVE: int = 4
    ANTELOPE_COLOR: Tuple[int, int, int] = (255, 0, 255)
    PLANT_INITIATIVE: int = 0
    GRASS_STRENGTH: int = 0
    GRASS_COLOR: Tuple[int, int, int] = (0, 255, 255)
    DANDELION_STRENGTH: int = 0
    DANDELION_COLOR: Tuple[int, int, int] = (255, 255, 0)
    GUARANA_STRENGTH: int = 0
    GUARANA_COLOR: Tuple[int, int, int] = (255, 255, 255)
    BELLADONNA_STRENGTH: int = 99
    BELLADONNA_COLOR: Tuple[int, int, int] = (255, 255, 255)
    HERACLEUM_SOSNOWSKYI_STRENGTH: int = 10
    HERACLEUM_SOSNOWSKYI_COLOR: Tuple[int, int, int] = (255, 255, 255)

    TURTLE_MOVE_CHANCE: float = 0.10
    TURTLE_REFLECTION_CHANCE: float = 0.25
    ANTELOPE_MOVE_RANGE: int = 2
    ANTELOPE_ESCAPE_CHANCE: float = 0.5
    PLANT_SPREAD_CHANCE: float = 0.1
    DANDELION_SPREAD_TRIES: int = 3
    GUARANA_STRENGTH_BOOST: int = 3

    HUMAN_ABILITY_COOLDOWN: int = 5
    HUMAN_ABILITY_DURATION: int = 5
