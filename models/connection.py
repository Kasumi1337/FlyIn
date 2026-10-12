from models.zone import Zone


class Connection:
    def __init__(
        self,
        zone_a: Zone,
        zone_b: Zone,
        max_link_capacity: int = 1,
    ) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
        self.current_usage: int = 0

    @property
    def has_capacity(self) -> bool:
        return self.current_usage < self.max_link_capacity

    def get_other(self, zone: Zone) -> Zone:
        if zone == self.zone_a:
            return self.zone_b
        if zone == self.zone_b:
            return self.zone_a
        raise ValueError(f"Zone {zone.name} is not part of this connection")

    def connects(self, zone_a: Zone, zone_b: Zone) -> bool:
        return (
            (self.zone_a == zone_a and self.zone_b == zone_b)
            or (self.zone_a == zone_b and self.zone_b == zone_a)
        )

    def __repr__(self) -> str:
        return (
            f"Connection({self.zone_a.name}"
            f"-{self.zone_b.name},"
            f" cap={self.max_link_capacity})"
        )
