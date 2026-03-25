from dataclasses import dataclass
from typing import Any
import datetime


@dataclass
class NodeMetaData:
    domain_name: str
    side: str
    robot_id: str
    name: str


@dataclass
class NodeData:
    info: NodeMetaData
    value: Any
    ts: datetime.datetime
