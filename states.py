from enum import auto, Enum

class PokemonStates(Enum):
    CAUGHT = auto()
    WILD = auto()


class TrainerStates(Enum):
    IDLE = auto()
    FIGHTING = auto()


class BattleStates(Enum):
    NOT_STARTED = auto()
    STARTED = auto()
    FINISHED = auto()