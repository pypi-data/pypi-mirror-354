from __future__ import annotations
from abc import ABC, abstractmethod
from typing import ClassVar
from collections import deque

from .types import Time, Motion, Color


__all__ = ['Style', 'Point', 'Circle', 'Line', 'Trail']


class Style:
	def __init__(self, color: Color, width: float, visible: bool) -> None:
		self.color = color
		self.width = width
		self.visible = visible


class Shape(ABC):
	objs: ClassVar[list[Shape]] = []

	@abstractmethod
	def __init__(self) -> None:
		type(self).objs.append(self)

	def refresh(self, t: Time) -> None:
		pass


class Point(Shape):
	default_style: ClassVar[Style] = Style(color="#FFFF00FF", width=8, visible=True)

	def __init__(self, motion: Motion, style: Style = default_style) -> None:
		super().__init__()
		self.motion = motion
		self.style = style
		self.refresh(0)

	def refresh(self, t: Time) -> None:
		self.x, self.y = self.motion(t)


class Circle(Shape):
	default_style: ClassVar[Style] = Style(color="#FFFFFFFF", width=1, visible=False)

	def __init__(self, center: Point, radius: float, style: Style = default_style) -> None:
		super().__init__()
		self.center = center
		self.radius = radius
		self.style = style


class Line(Shape):
	default_style: ClassVar[Style] = Style(color="#0000FFFF", width=1, visible=True)

	def __init__(self, p1: Point, p2: Point, style: Style = default_style) -> None:
		super().__init__()
		self.p1 = p1
		self.p2 = p2
		self.style = style
		self.refresh(0)

	def refresh(self, t: Time) -> None:
		self.a = self.p1.y - self.p2.y
		self.b = self.p2.x - self.p1.x
		self.c = self.p1.x * self.p2.y - self.p2.x * self.p1.y


class Trail(Shape):
	default_line_style: ClassVar[Style] = Style(color="#FFFF00FF", width=1, visible=True)
	default_point_style: ClassVar[Style] = Style(color="#FFFF00FF", width=1, visible=False)

	def __init__(
		self, point: Point, length: int, step: int = 1,
		line_style: Style = default_line_style,
		point_style: Style = default_point_style
	) -> None:
		super().__init__()
		self.point = point
		self.step = step
		self.line_style = line_style
		self.point_style = point_style
		self.history = {'x': deque(maxlen=length), 'y': deque(maxlen=length)}
		self.counter = -1
		self.refresh(0)

	def refresh(self, t: Time) -> None:
		self.counter = (self.counter + 1) % self.step
		if self.counter != 0:
			return
		self.history['x'].append(self.point.x)
		self.history['y'].append(self.point.y)
