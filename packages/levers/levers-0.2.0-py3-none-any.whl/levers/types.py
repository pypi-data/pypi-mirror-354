type Time = float
type Position = tuple[float, float]
type Motion = Callable[[Time], Position]
type Selector = Callable[[Position, Position], Position]
type Color = str
