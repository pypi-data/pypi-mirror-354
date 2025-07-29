from math import sin, cos, hypot, sqrt, pi, radians
from typing import Callable

from .types import Time, Position, Motion, Selector
from .geometry import Point, Line, Circle
from .selectors import lower_left as default_selector


__all__ = ['static', 'rotating', 'sliding', 'on_intersection', 'on_line', 'on_angle_side']


def static(x: float, y: float) -> Motion:
	def f(t: Time) -> Position:
		return (x, y)
	return f

def rotating(x: float, y: float, r: float, f: float) -> Motion:
	def func(t: Time) -> Position:
		common = 2 * pi * t * f
		return (r * sin(common) + x, r * cos(common) + y)
	return func

def sliding(x1: float, y1: float, x2: float, y2: float, f: float) -> Motion:
	def func(t: Time) -> Position:
		mid_x = (x1 + x2) / 2
		mid_y = (y1 + y2) / 2
		dx = x2 - x1
		dy = y2 - y1
		common = cos(2 * pi * t * f) / 2
		return (dx * common + mid_x, dy * common + mid_y)
	return func

def ll_intersect(a: Line, b: Line) -> Motion:
	def f(t: Time) -> Position:
		z = a.a * b.b - b.a * a.b
		if z == 0:
			raise ValueError("Lines do not intersect or are identical.")
		x = (a.b * b.c - b.b * a.c) / z
		y = (b.a * a.c - a.a * b.c) / z
		return (x, y)
	return f

def cl_intersect(circ: Circle, line: Line, select: Selector = default_selector) -> Motion:
	def f(t: Time) -> Position:
		a, b, c = line.a, line.b, line.c
		r, v, w = circ.radius, circ.center.x, circ.center.y
		
		if a != 0:
			z = -a**2*(-a**2*r**2+a**2*v**2+2*a*b*v*w+2*a*c*v-b**2*r**2+b**2*w**2+2*b*c*w+c**2)
			if z < 0:
				raise ValueError("Line and circle do not intersect.")
			y1 = (sqrt(z)+a**2*w-a*b*v-b*c)/(a**2+b**2)
			y2 = (-sqrt(z)+a**2*w-a*b*v-b*c)/(a**2+b**2)
			x1 = -(b*y1+c)/a
			x2 = -(b*y2+c)/a
		
		else:
			z = -b**2*(b**2*(w**2-r**2)+2*b*c*w+c**2)
			if z < 0:
				raise ValueError("Line and circle do not intersect.")
			x1 = v-sqrt(z)/b**2
			x2 = (sqrt(z)+b**2*v)/b**2
			y1 = -(a*x1+c)/b
			y2 = -(a*x2+c)/b
		
		return select((x1, y1), (x2, y2))

	return f

def cc_intersect(a: Circle, b: Circle, select: Selector = default_selector) -> Motion:
	def f(t: Time) -> Position:
		r2, v, w = a.radius**2, a.center.x, a.center.y
		R2, V, W = b.radius**2, b.center.x, b.center.y
		dv = v - V
		dw = w - W

		if dv == 0 and dw == 0:
			raise ValueError("Cannot find intersection of concentric circles")

		elif dw != 0:
			d = 2 * ((dv)**2 + (dw)**2)
			z = -dw**2 * ((r2 - R2)**2 - 2 * (r2 + R2 - dw**2) * dv**2 + dv**4 + dw**4 - 2 * (r2 + R2) * dw**2)

			if z < 0:
				raise ValueError("Circles do not intersect")

			x_common = (R2 - r2 + v**2 - V**2) * (dv) + (v + V)*dw**2
			x1 = (x_common - sqrt(z)) / d
			x2 = (x_common + sqrt(z)) / d

			y_common = (R2 - r2) * dw**2 + (w**2 - W**2) * dv**2 + dw**3 * (w + W)
			y1 = (y_common + dv * sqrt(z)) / (dw * d)
			y2 = (y_common - dv * sqrt(z)) / (dw * d)

		else:
			x = x1 = x2 = (R2 - r2 + v**2 - V**2) / (2 * dv)

			z = 2*v*x - x**2 + r2 - v**2

			if z < 0:
				raise ValueError("Circles do not intersect")

			y1 = w - sqrt(z)
			y2 = w + sqrt(z)

		return select((x1, y1), (x2, y2))

	return f

def on_intersection(a: Circle | Line, b: Circle | Line, select: Selector = default_selector) -> Motion:
	if isinstance(a, Circle) and isinstance(b, Circle):	
		return cc_intersect(a, b, select)
	elif isinstance(a, Line) and isinstance(b, Line):
		return ll_intersect(a, b)
	elif isinstance(a, Circle) and isinstance(b, Line):
		return cl_intersect(a, b, select)
	elif isinstance(a, Line) and isinstance(b, Circle):
		return cl_intersect(b, a, select)
	else:
		raise TypeError(
			f"Can only intersect lines and circles, got {type(a).__name__} and {type(b).__name__}"
		)

def on_line(a: Point, b: Point, dist_from_a: float) -> Motion:
	if a.x == b.x and a.y == b.y:
		raise ValueError('A line cannot be defined by two coincident points')
	def f(t: Time) -> Position:
		dx = b.x - a.x
		dy = b.y - a.y
		k = dist_from_a / hypot(dx, dy)
		return (dx * k + a.x, dy * k + a.y)
	return f

def on_angle_side(a: Point, b: Point, angle_deg: float, dist_from_a: float) -> Motion:
	if a.x == b.x and a.y == b.y:
		raise ValueError('An angle side cannot be defined by two coincident points')
	def f(t: Time) -> Position:
		dx = b.x - a.x
		dy = b.y - a.y
		length = hypot(dx, dy)
		ux, uy = dx / length, dy / length
		theta = radians(angle_deg)
		rx = ux * cos(theta) - uy * sin(theta)
		ry = ux * sin(theta) + uy * cos(theta)
		return (a.x + dist_from_a * rx, a.y + dist_from_a * ry)
	return f