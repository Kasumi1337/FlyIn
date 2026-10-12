from models.graph import Graph
from models.drone import Drone
from models.zone import Zone


class Simulator:
    def __init__(
            self,
            graph: Graph,
            drones: list[Drone],
            paths: list[list[Zone]]
            ) -> None:
        self.graph = graph
        self.drones = drones
        self.paths = paths

    def run(self) -> int:
        counter = 0
        while not all(drone.arrived for drone in self.drones):
            counter += 1
            moves = self.step()
            print(self.format_turn(moves))
        return counter

    def step(self) -> list[tuple[Drone, Zone]]:
        moves = []
        for i, drone in enumerate(self.drones):
            if drone.arrived:
                continue
            next_zone = self.paths[i][drone.path_index + 1]
            if not next_zone.has_capacity:
                continue
            link = self.graph.get_connection(drone.pos, next_zone)
            if link is None or not link.has_capacity:
                continue
            link.current_usage += 1
            drone.pos.current_drones -= 1
            next_zone.current_drones += 1
            moves.append((drone, next_zone))
            drone.move(next_zone)
            drone.path_index += 1
            if drone.pos == self.graph.end:
                drone.mark_arrived()
        for conn in self.graph.connections:
            conn.current_usage = 0
        return moves

    def format_turn(self, move: list[tuple[Drone, Zone]]) -> str:
        parts = []
        for i in move:
            drone, zone = i
            parts.append(str(drone) + "-" + zone.name)
        return " ".join(parts)
