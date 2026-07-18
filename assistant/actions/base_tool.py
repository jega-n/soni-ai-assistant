from abc import ABC, abstractmethod
from enum import Enum


class ToolType(Enum):
    DETERMINISTIC = "deterministic"
    REASONING = "reasoning"


class BaseTool(ABC):
    name = ""
    description = ""
    tool_type = ToolType.DETERMINISTIC

    @abstractmethod
    def execute(self, **kwargs):
        pass