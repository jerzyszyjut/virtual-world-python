from typing import Tuple


class Config:
    WORLD_WIDTH: int = 40
    WORLD_HEIGHT: int = 40

    HUMAN_STRENGTH: int = 5
    HUMAN_INITIATIVE: int = 4
    HUMAN_COLOR: Tuple[int, int, int] = (255, 219, 172)
    WOLF_STRENGTH: int = 9
    WOLF_INITIATIVE: int = 5
    WOLF_COLOR: Tuple[int, int, int] = (220, 220, 220)
    SHEEP_STRENGTH: int = 4
    SHEEP_INITIATIVE: int = 4
    SHEEP_COLOR: Tuple[int, int, int] = (255, 255, 255)
    FOX_STRENGTH: int = 3
    FOX_INITIATIVE: int = 7
    FOX_COLOR: Tuple[int, int, int] = (183, 88, 0)
    TURTLE_STRENGTH: int = 2
    TURTLE_INITIATIVE: int = 1
    TURTLE_COLOR: Tuple[int, int, int] = (0, 255, 0)
    ANTELOPE_STRENGTH: int = 4
    ANTELOPE_INITIATIVE: int = 4
    ANTELOPE_COLOR: Tuple[int, int, int] = (177, 150, 100)
    CYBER_SHEEP_STRENGTH: int = 11
    CYBER_SHEEP_INITIATIVE: int = 4
    CYBER_SHEEP_COLOR: Tuple[int, int, int] = (122, 123, 119)
    PLANT_INITIATIVE: int = 0
    GRASS_STRENGTH: int = 0
    GRASS_COLOR: Tuple[int, int, int] = (0, 128, 0)
    DANDELION_STRENGTH: int = 0
    DANDELION_COLOR: Tuple[int, int, int] = (255, 255, 0)
    GUARANA_STRENGTH: int = 0
    GUARANA_COLOR: Tuple[int, int, int] = (37, 150, 190)
    BELLADONNA_STRENGTH: int = 99
    BELLADONNA_COLOR: Tuple[int, int, int] = (0, 0, 0)
    HERACLEUM_SOSNOWSKYI_STRENGTH: int = 10
    HERACLEUM_SOSNOWSKYI_COLOR: Tuple[int, int, int] = (102, 116, 75)

    TURTLE_MOVE_CHANCE: float = 0.10
    TURTLE_REFLECTION_STRENGTH: int = 5
    ANTELOPE_MOVE_RANGE: int = 2
    ANTELOPE_ESCAPE_CHANCE: float = 0.5
    PLANT_SPREAD_CHANCE: float = 0.1
    DANDELION_SPREAD_TRIES: int = 3
    GUARANA_STRENGTH_BOOST: int = 3

    HUMAN_ABILITY_COOLDOWN: int = 5
    HUMAN_ABILITY_DURATION: int = 5

    HUMAN_DEFAULT_POSITION: Tuple[int, int] = (0, 0)

    SAVE_FILE_NAME: str = "save.json"
    LOAD_FILE_NAME: str = SAVE_FILE_NAME

    BASE_FIELD_SIZE: int = 20
    WORLD_WINDOW_WIDTH: int = 1000
    WORLD_WINDOW_HEIGHT: int = 1000
