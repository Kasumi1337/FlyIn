from typing import Optional
from models.zone import Zone
from models.connection import Connection


class Graph:
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start: Optional[Zone] = None
        self.end: Optional[Zone] = None

    def add_zone(self, zone: Zone) -> None:
        if zone.name in self.zones:
            raise ValueError
        self.zones[zone.name] = zone

    def add_connection(self, conn: Connection) -> None:
        self.connections.append(conn)

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        res = []
        for i in self.connections:
            if zone == i.zone_a or zone == i.zone_b:
                res.append(i.get_other(zone))
        return res

    def get_connection(self, zone_a: Zone,
                       zone_b: Zone) -> Optional[Connection]:
        for conn in self.connections:
            if conn.connects(zone_a, zone_b):
                return conn
        return None
