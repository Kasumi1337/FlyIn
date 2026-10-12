from enum import Enum
from typing import Optional


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    @property
    def move_cost(self) -> int:
        if self == ZoneType.RESTRICTED:
            return 2
        return 1


class Zone:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: Optional[str] = None,
        max_drones: int = 1,
        is_start: bool = False,
        is_end: bool = False,
        extra_cost: int = 0
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.is_start = is_start
        self.is_end = is_end
        self.current_drones: int = 0
        self.extra_cost = extra_cost

    @property
    def is_accessible(self) -> bool:
        return self.zone_type != ZoneType.BLOCKED

    @property
    def has_capacity(self) -> bool:
        if self.is_end:
            return True
        return self.current_drones < self.max_drones

    def __repr__(self) -> str:
        return f"Zone({self.name}, {self.zone_type.value})"
