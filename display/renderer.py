from models.graph import Graph
from models.drone import Drone
from models.zone import Zone
from simulation.simulator import Simulator
import tkinter as tk


class Renderer:
    def __init__(
            self,
            path: list[list[Zone]],
            drones: list[Drone],
            graph: Graph,
            simulator: Simulator,
            ):
        self.path = path
        self.drones = drones
        self.graph = graph
        self.turn = 0
        self.simulator = simulator
        self.root = tk.Tk()
        self.root.title("Fly-in")
        self.canvas = tk.Canvas(self.root, width=6400, height=3400, bg="white")
        self.canvas.pack()

    def get_screen_pos(self, zone: Zone) -> tuple[int, int]:
        min_x = min(z.x for z in self.graph.zones.values())
        min_y = min(z.y for z in self.graph.zones.values())
        x = (zone.x - min_x) * 150 + 600
        y = (zone.y - min_y) * 450 + 500
        return x, y

    def render(self) -> None:
        self.canvas.create_text(150, 50, text=f"Turn: {self.turn}",
                                font=("Arial", 16))
        for conn in self.graph.connections:
            x1, y1 = self.get_screen_pos(conn.zone_a)
            x2, y2 = self.get_screen_pos(conn.zone_b)
            self.canvas.create_line(x1, y1, x2, y2, fill="black")
        for zone in self.graph.zones.values():
            x, y = self.get_screen_pos(zone)
            color = zone.color if zone.color else "blue"
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
            self.canvas.create_text(x, y - 30, text=zone.name)
        self.root.after(1000, self.animate_step)
        self.root.mainloop()

    def animate_step(self) -> None:
        moves = self.simulator.step()
        print(self.simulator.format_turn(moves))
        self.turn += 1
        self.canvas.delete("all")
        self.canvas.create_text(150, 50, text=f"Turn: {self.turn}",
                                font=("Arial", 16))
        for conn in self.graph.connections:
            x1, y1 = self.get_screen_pos(conn.zone_a)
            x2, y2 = self.get_screen_pos(conn.zone_b)
            self.canvas.create_line(x1, y1, x2, y2, fill="black")
        for zone in self.graph.zones.values():
            x, y = self.get_screen_pos(zone)
            color = zone.color if zone.color else "blue"
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
            self.canvas.create_text(x, y - 30, text=zone.name)
        for drone in self.drones:
            if not drone.arrived:
                x, y = self.get_screen_pos(drone.pos)
                self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="white")
                self.canvas.create_text(x, y + 30, text=str(drone))
        if not all(drone.arrived for drone in self.drones):
            self.root.after(1000, self.animate_step)
        else:
            print(f"Total turns: {self.turn}")
            self.root.destroy()
