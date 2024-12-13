from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    DIFFICULTY_SELECT = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    SETTINGS = auto()