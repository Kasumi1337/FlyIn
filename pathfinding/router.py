from models.zone import Zone, ZoneType
from models.graph import Graph


class Rooter:
    def __init__(self) -> None:
        pass

    def find_path(self, start: Zone, end: Zone, graph: Graph) -> list[Zone]:
        distances: dict[str, float] = {}
        previous: dict[str, Zone | None] = {}
        to_visit = [(0, 0, start)]
        counter = 0
        for name, zone in graph.zones.items():
            distances[name] = float('inf')
            previous[name] = None

        distances[start.name] = 0
        while to_visit:
            to_visit.sort()
            counter += 1
            cost, _, current = to_visit.pop(0)
            if current == end:
                path = []
                current_node: Zone | None = end
                while current_node is not None:
                    counter += 1
                    path.append(current_node)
                    current_node = previous[current_node.name]
                path = path[::-1]
                return path
            else:
                for voisin in graph.get_neighbors(current):
                    if voisin.zone_type == ZoneType.BLOCKED:
                        continue
                    new_cost = cost + voisin.zone_type.move_cost + \
                        voisin.extra_cost
                    if new_cost < distances[voisin.name]:
                        distances[voisin.name] = new_cost
                        previous[voisin.name] = current
                        counter += 1
                        to_visit.append((new_cost, counter, voisin))
        return []

    def find_multiple_paths(self, start: Zone, end: Zone, graph: Graph,
                            nb_drones: int) -> list[list[Zone]]:
        path = []
        for i in range(nb_drones):
            chemin = self.find_path(start, end, graph)
            if not chemin:
                break
            path.append(chemin)
            for zone in chemin[1:-1]:
                zone.extra_cost += 10
        return path
