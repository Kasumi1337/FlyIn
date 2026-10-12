from models.zone import Zone


class Drone:
    def __init__(
            self,
            id: int,
            pos: Zone,
            ) -> None:
        self.id = id
        self.pos = pos
        self.path_index = 0
        self.way: list[Zone] = []
        self.arrived: bool = False
        self.in_transit: bool = False

    def move(self, zone: Zone) -> None:
        self.pos = zone

    def mark_arrived(self) -> None:
        if not self.arrived:
            self.arrived = True

    def __repr__(self) -> str:
        return ("D" + str(self.id))
