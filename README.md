
*This project was created as part of the 42 curriculum by thbeil.*

# Fly-in 🚁

---

## Description

**Fly-in** is a drone routing simulation project. Given a network of zones represented as a graph, the program routes a fleet of drones from a start zone to an end zone in the fewest possible simulation turns.

The project includes:
- A **parser** that reads custom map files defining zones, connections, and constraints
- A **pathfinding algorithm** to compute optimal routes for each drone
- A **simulation engine** that moves drones turn by turn while respecting occupancy and capacity rules
- A **graphical interface** to visualize the simulation in real time

The project is written entirely in Python and follows strict **Object-Oriented Programming** principles, with full type safety enforced by `mypy` and `flake8`.

---

## Instructions

### Installation
```bash
make install
```

### Run
```bash
python3 main.py <path_to_map>
```
Or edit the `NAME` variable in the `Makefile` and run:
```bash
make run
```

### Lint
```bash
make lint         # standard check
make lint-strict  # strict mypy check
```

### Debug
```bash
make debug
```

### Clean
```bash
make clean
```

---

## Algorithm

The pathfinding algorithm used is **Dijkstra's algorithm**, adapted for weighted graphs with zone-type costs:

- `normal` zones cost **1 turn**
- `restricted` zones cost **2 turns**
- `priority` zones cost **1 turn** but are preferred by the algorithm
- `blocked` zones are **inaccessible**

To distribute drones across multiple paths, the algorithm runs repeatedly, incrementally increasing the cost of already-used intermediate zones (`extra_cost`). This encourages subsequent drones to find alternative routes, improving overall throughput.

Drones move simultaneously each turn, and the simulation respects zone capacity (`max_drones`) and connection capacity (`max_link_capacity`) constraints.

---

## Visual Representation

The graphical interface is built with **tkinter**:

- **Zones** are displayed as colored circles (colors defined in the map file)
- **Connections** are drawn as lines between zones
- **Drones** appear as white circles labeled with their ID (e.g. `D1`, `D2`)
- The simulation animates **turn by turn** with a 1-second delay between each step
- A **turn counter** is displayed in the upper-left corner

---

## Resources

- [Dijkstra's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python tkinter documentation](https://docs.python.org/3/library/tkinter.html)
- [Python typing module](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)

### AI Usage

Claude (Anthropic) was used throughout this project as a learning assistant:
- To understand and structure the OOP architecture
- To debug mypy and flake8 errors
- To review and improve code quality

All code was written, understood, and validated by the author.