import os
from time import time

import pyqtgraph as pg
from pyqtgraph.exporters import ImageExporter
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QGraphicsEllipseItem

from ..geometry import Point, Line, Circle, Trail
from .renderer import Renderer


class PyQtGraphRenderer(Renderer):
    def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float, ppu: float) -> None:
        self.plt = pg.plot(title='Levers')
        self.plt.showGrid(x=True, y=True)
        self.plt.getAxis('bottom').setZValue(-1)
        self.plt.getAxis('left').setZValue(-1)
        self.plt.setAspectLocked()
        self.plt.disableAutoRange()

        self.plt.setGeometry(100, 100, int(ppu*(xmax-xmin)) , int(ppu*(ymax-ymin)))
        self.plt.setXRange(xmin, xmax)
        self.plt.setYRange(ymin, ymax)

    def run(self, fps: float) -> None:
        self.start_time = time()
        self.mspf = int(1000 / fps)

        self.next_frame_run()
        pg.exec()

    def next_frame_run(self) -> None:
        QTimer.singleShot(self.mspf, self.next_frame_run)

        self.plt.clear()
        self.scatter=pg.ScatterPlotItem()
        self.scatter.setZValue(1)
        self.plt.addItem(self.scatter)
        self.draw_all(time() - self.start_time)

    def capture(self, fps: float, frames: int, path: str) -> None:
        self.spf = 1 / fps
        self.frame = -10
        self.max_frame = frames
        self.folder = path

        self.exporter = ImageExporter(self.plt.plotItem)
        os.makedirs(self.folder, exist_ok=True)

        self.next_frame_capture()
        pg.exec()

    def next_frame_capture(self) -> None:
        QTimer.singleShot(0, self.next_frame_capture)

        self.plt.clear()
        self.scatter=pg.ScatterPlotItem()
        self.scatter.setZValue(1)
        self.plt.addItem(self.scatter)
        self.draw_all(self.frame * self.spf)
        if self.frame >= 0: 
            self.exporter.export(os.path.join(self.folder, f'{self.frame}.png'))

        self.frame += 1
        if self.frame == self.max_frame: exit()

    def draw_point(self, point: Point) -> None:
        if point.style.visible == False:
            return
        self.scatter.addPoints(
            pos=((point.x, point.y),), 
            pen=None, 
            brush=point.style.color, 
            size=point.style.width
        )

    def draw_line(self, line: Line) -> None:
        if line.style.visible == False:
            return
        self.plt.plot(
            (line.p1.x, line.p2.x), 
            (line.p1.y, line.p2.y), 
            pen=pg.mkPen(line.style.color, width=line.style.width)
        )

    def draw_circle(self, circle: Circle) -> None:
        if circle.style.visible == False:
            return
        p_ellipse = QGraphicsEllipseItem(
            circle.center.x - circle.radius, 
            circle.center.y - circle.radius, 
            circle.radius*2, 
            circle.radius*2
        )
        p_ellipse.setPen(pg.mkPen(circle.style.color))
        self.plt.addItem(p_ellipse)

    def draw_trail(self, trail: Trail) -> None:
        if not trail.line_style.visible and not trail.point_style.visible:
            return
        if trail.line_style.visible:
            pen = pg.mkPen(trail.line_style.color, width=trail.line_style.width)
        else:
            pen = None
        self.plt.plot(
            trail.history, 
            pen=pen,
            symbol='o' if trail.point_style.visible else None,
            symbolPen=None,
            symbolBrush=trail.point_style.color,
            symbolSize=trail.point_style.width
        ).setZValue(-0.5)
