from enum import Enum


class ActionType(str, Enum):
    CHAT = "CHAT"
    DETERMINISTIC = "DETERMINISTIC"
    REASONING = "REASONING"