from dataclasses import dataclass
from datetime import datetime

@dataclass
class Memory:

    memory_type: str
    content: str
    timestamp: datetime = datetime.now()
    importance: int = 1