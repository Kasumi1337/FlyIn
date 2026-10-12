from models.graph import Graph
from models.zone import Zone, ZoneType
from models.connection import Connection


class MapParser:
    def __init__(
            self,
            filepath: str
            ) -> None:
        self.filepath: str = filepath

    def parse(self) -> tuple[Graph, int]:
        res = Graph()
        counter = 0
        with open(self.filepath, "r") as file:
            for line in file:
                counter += 1
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("nb_drones:"):
                    try:
                        nb_drone = int(line.split(": ")[1])
                        if nb_drone <= 0:
                            raise ParseError(counter, "nb_drones must be a \
                                             positive integer")
                    except (ValueError, IndexError):
                        raise ParseError(counter, "nb_drones must be an\
                                              integer")
                elif line.startswith("start_hub:"):
                    start_zone = self.parse_zone(line, counter)
                    start_zone.is_start = True
                    if res.start is not None:
                        raise ParseError(counter, "duplicate start_hub")
                    try:
                        res.add_zone(start_zone)
                    except ValueError:
                        raise ParseError(counter, f"duplicate zone name\
                                          '{start_zone.name}'")
                    res.start = start_zone
                    try:
                        if res.start and res.start.max_drones == 1:
                            res.start.max_drones = nb_drone
                    except UnboundLocalError:
                        raise ParseError(counter, "Need drone number")

                elif line.startswith("end_hub:"):
                    end_zone = self.parse_zone(line, counter)
                    end_zone.is_end = True
                    if res.end is not None:
                        raise ParseError(counter, "duplicate end_hub")
                    try:
                        res.add_zone(end_zone)
                    except ValueError:
                        raise ParseError(counter, f"duplicate zone name\
                                          '{end_zone.name}'")
                    res.end = end_zone
                elif line.startswith("hub:"):
                    hub = self.parse_zone(line, counter)
                    try:
                        res.add_zone(hub)
                    except ValueError:
                        raise ParseError(counter, f"duplicate hub name\
                                        '{hub.name}'")
                elif line.startswith("connection:"):
                    conn = self.parse_connection(line, res, counter)
                    res.add_connection(conn)
            try:
                if res.start and res.start.max_drones < nb_drone:
                    raise ParseError(counter,
                                     "nb_drones exceeds start zone capacity")
            except UnboundLocalError:
                raise ParseError(counter, "Need drone number")
            return (res, nb_drone)

    def parse_zone(self, line: str, line_num: int) -> Zone:
        content: str = line.split(": ", 1)[1]
        parts: list[str] = content.split(" ", 3)
        name = parts[0]
        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            raise ParseError(line_num, "Need x, y")
        zone = ZoneType("normal")
        color = None
        max_drones = 1
        try:
            metadata_str: str = parts[3].strip("[").strip("]")
            metadata: list[str] = metadata_str.split(" ")
            for item in metadata:
                key, value = item.split("=")
                if key == "zone":
                    try:
                        zone = ZoneType(value)
                    except ValueError:
                        raise ParseError(line_num, "wrong ZoneType value")
                if key == "color":
                    if value != "rainbow":
                        color = value
                    else:
                        color = "black"
                if key == "max_drones":
                    max_drones = int(value)
        except IndexError:
            pass
        res = Zone(name, x, y, zone, color, max_drones)
        return res

    def parse_connection(self, line: str, graph: Graph,
                         line_num: int) -> Connection:
        part = line.split(" ")
        zone_a, zone_b = part[1].split("-")
        max_link = 1
        try:
            parts: str = part[2].strip("]").strip("[")
            parts_list: list[str] = parts.split("=")
            max_link = int(parts_list[1])
        except IndexError:
            pass
        if zone_a not in graph.zones:
            raise ParseError(line_num, f"undefined zone '{zone_a}'")
        if zone_b not in graph.zones:
            raise ParseError(line_num, f"undefined zone '{zone_b}'")
        for conn in graph.connections:
            if conn.connects(graph.zones[zone_a], graph.zones[zone_b]):
                raise ParseError(line_num, "duplicate connection")
        try:
            res = Connection(graph.zones[zone_a],
                             graph.zones[zone_b], max_link)
        except KeyError as e:
            raise ParseError(line_num, f"undefined zone {e}")
        return res


class ParseError(Exception):
    def __init__(self, line_num: int, message: str) -> None:
        self.line_num = line_num
        self.message = message

        print(f"Error line {line_num}: {message}")
