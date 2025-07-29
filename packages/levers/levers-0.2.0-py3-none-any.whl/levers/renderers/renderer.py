from abc import ABC, abstractmethod

from ..geometry import Shape, Point, Line, Circle, Trail
from ..types import Time


class Renderer(ABC):
    @abstractmethod
    def draw_point(self, point: Point) -> None: pass

    @abstractmethod
    def draw_line(self, line: Line) -> None: pass

    @abstractmethod
    def draw_circle(self, circle: Circle) -> None: pass

    @abstractmethod
    def draw_trail(self, trail: Trail) -> None: pass

    def draw_all(self, t: Time) -> None:
        for o in Shape.objs:
            o.refresh(t)
            if isinstance(o, Point): 
                self.draw_point(o)
            elif isinstance(o, Circle): 
                self.draw_circle(o)
            elif isinstance(o, Line): 
                self.draw_line(o)
            elif isinstance(o, Trail):
                self.draw_trail(o)
            else:
                raise RuntimeError(f"Unexpected shape type: {type(o).__name__}")

    @abstractmethod
    def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float, ppu: float) -> None: pass

    @abstractmethod
    def run(self, fps: float) -> None: pass

    def capture(self, fps: float, frames: int, path: str) -> None:
        raise NotImplementedError("Capture method is not implemented for this class")
