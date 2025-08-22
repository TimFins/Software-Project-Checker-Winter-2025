from enum import Enum, auto


class BSTViolationType(Enum):
    TOO_SMALL_FOR_RIGHT_SUBTREE = auto()
    TOO_LARGE_FOR_LEFT_SUBTREE = auto()
