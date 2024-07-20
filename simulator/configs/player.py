from enum import Enum, auto


class Position(Enum):
    ATTACKER = auto()
    MIDFIELDER = auto()
    DEFENDER = auto()
    GOALKEEPER = auto()


class TeamStatus(Enum):
    STARTER = auto()
    SUBSTITUTE = auto()
    RESERVE = auto()
