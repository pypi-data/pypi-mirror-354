from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MCPServerConfig:
    name: str
    command: str
    args: List[str]
    env: Dict[str, str] = None


@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: float
