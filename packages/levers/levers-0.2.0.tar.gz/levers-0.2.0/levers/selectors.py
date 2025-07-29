from .types import Position, Selector
from .geometry import Point


__all__ = [
	'lower_left', 'lower_right', 'upper_left', 'upper_right',
	'left_upper', 'left_lower', 'right_upper', 'right_lower',
	'closest_to', 'furthest_from',
	'most_clockwise_from', 'most_counterclockwise_from'
]


def lower_left(a: Position, b: Position) -> Position:
	return min(a, b, key=lambda x: (x[1], x[0]))

def lower_right(a: Position, b: Position) -> Position:
	return min(a, b, key=lambda x: (x[1], -x[0]))

def upper_left(a: Position, b: Position) -> Position:
	return max(a, b, key=lambda x: (x[1], -x[0]))

def upper_right(a: Position, b: Position) -> Position:
	return max(a, b, key=lambda x: (x[1], x[0]))

def left_upper(a: Position, b: Position) -> Position:
	return min(a, b, key=lambda x: (x[0], -x[1]))

def left_lower(a: Position, b: Position) -> Position:
	return min(a, b)

def right_upper(a: Position, b: Position) -> Position:
	return max(a, b)

def right_lower(a: Position, b: Position) -> Position:
	return max(a, b, key=lambda x: (x[0], -x[1]))

def closest_to(o: Position|Point) -> Selector:
	if isinstance(o, Point):
		def f(a: Position, b: Position) -> Position:
			return min(a, b, key = lambda x: hypot(x[0] - o.x, x[1] - o.y))
	elif isinstance(o, tuple):
		def f(a: Position, b: Position) -> Position:
			return min(a, b, key = lambda x: hypot(x[0] - o[0], x[1] - o[1]))
	else:
		raise TypeError(
			f'Unsupported argument type. Expected: Position or Point, got: {type(o).__name__}'
		)
	return f

def furthest_from(o: Position|Point) -> Selector:
	if isinstance(o, Point):
		def f(a: Position, b: Position) -> Position:
			return max(a, b, key = lambda x: hypot(x[0] - o.x, x[1] - o.y))
	elif isinstance(o, tuple):
		def f(a: Position, b: Position) -> Position:
			return max(a, b, key = lambda x: hypot(x[0] - o[0], x[1] - o[1]))
	else:
		raise TypeError(
			f'Unsupported argument type. Expected: Position or Point, got: {type(o).__name__}'
		)
	return f

def most_clockwise_from(o: Position|Point) -> Selector:
	if isinstance(o, Point):
		def f(a: Position, b: Position) -> Position:
			oa = (a[0] - o.x, a[1] - o.y)
			ob = (b[0] - o.x, b[1] - o.y)
			if oa[0] * ob[1] - oa[1] * ob[0] > 0:
				return a
			else:
				return b
	elif isinstance(o, tuple):
		def f(a: Position, b: Position) -> Position:
			oa = (a[0] - o[0], a[1] - o[1])
			ob = (b[0] - o[0], b[1] - o[1])
			if oa[0] * ob[1] - oa[1] * ob[0] > 0:
				return a
			else:
				return b
	else:
		raise TypeError(
			f'Unsupported argument type. Expected: Position or Point, got: {type(o).__name__}'
		)
	return f

def most_counterclockwise_from(o: Position|Point) -> Selector:
	if isinstance(o, Point):
		def f(a: Position, b: Position) -> Position:
			oa = (a[0] - o.x, a[1] - o.y)
			ob = (b[0] - o.x, b[1] - o.y)
			if oa[0] * ob[1] - oa[1] * ob[0] < 0:
				return a
			else:
				return b
	elif isinstance(o, tuple):
		def f(a: Position, b: Position) -> Position:
			oa = (a[0] - o[0], a[1] - o[1])
			ob = (b[0] - o[0], b[1] - o[1])
			if oa[0] * ob[1] - oa[1] * ob[0] < 0:
				return a
			else:
				return b
	else:
		raise TypeError(
			f'Unsupported argument type. Expected: Position or Point, got: {type(o).__name__}'
		)
	return f
