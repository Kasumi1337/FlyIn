from parser.map_parser import MapParser, ParseError
from pathfinding.router import Rooter
from models.drone import Drone
from simulation.simulator import Simulator
from display.renderer import Renderer
import sys


def main() -> None:
    if len(sys.argv) < 2:
        ("Usage: python3 main.py <map_file>")
        sys.exit(1)
    parser = MapParser(sys.argv[1])
    try:
        graph, nb_drones = parser.parse()
    except ParseError as e:
        (e)
        sys.exit(1)
    if graph.start is None or graph.end is None:
        print("Error: missing start or end zone")
        sys.exit(1)
    graph.start.current_drones = nb_drones
    router = Rooter()
    try:
        path = router.find_multiple_paths(graph.start, graph.end,
                                          graph, nb_drones)
        drones = [Drone(i + 1, graph.start) for i in range(nb_drones)]
        paths = [path[i % len(path)] for i in range(nb_drones)]
        simulator = Simulator(graph, drones, paths)
        renderer = Renderer(paths, drones, graph, simulator)
    except (ZeroDivisionError, ParseError, UnboundLocalError) as e:
        print(e)

    try:
        renderer.render()
    except KeyboardInterrupt:
        renderer.root.destroy()
    except (UnboundLocalError, TypeError) as e:
        print(e)

if __name__ == "__main__":
    main()
