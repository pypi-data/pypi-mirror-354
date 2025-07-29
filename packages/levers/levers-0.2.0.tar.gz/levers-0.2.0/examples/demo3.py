### This is a model of Chebyshev long-dwell linkage
### In this file, we avoid using keyword arguments unnecessarily.

### We recommend to import Levers core like this to make your code less noisy
from levers import *

### Import one of the renderers you want to use
from levers.renderers import PyQtGraphRenderer
# from levers.renderers import PyGameRenderer


red_line = Style(color="#FF0000FF", width=1, visible=True)

### Static points
O = Point(static(0.645, 0.402))
C = Point(static(0, 0))
F = Point(static(-1.6552, -0.12578))

### Moving points
A = Point(rotating(O.x, O.y, 0.305, 0.33))
circ_A = Circle(A, 1)
circ_C = Circle(C, 1)
B = Point(on_intersection(circ_A, circ_C, upper_left))
M = Point(on_angle_side(B, A, -114, 1))
circ_M = Circle(M, 0.66)
circ_F = Circle(F, 0.8)
D = Point(on_intersection(circ_M, circ_F, upper_left))
W = Point(on_line(D, F, -1))

### Lines
Line(A, O)
Line(B, C)
Line(A, B, style=red_line)
Line(B, M, style=red_line)
Line(M, D)
Line(W, F, style=red_line)

### Render the animation using the renderer imported above
PyQtGraphRenderer(-2.75, 1.5, -0.75, 2, 150).run(60)
# PyGameRenderer(-2.75, 1.5, -0.75, 2, 150).run(60)

### Or capture the frames and save them to a folder
# PyQtGraphRenderer(-2.75, 1.5, -0.75, 2, 150).capture(60, 180, 'capture_folder')
# PyGameRenderer(-2.75, 1.5, -0.75, 2, 150).capture(60, 180, 'capture_folder')
