# This is a model of Chebyshev lambda linkage.
# In this file, we use keyword arguments even where it is not necessary.
# For a more concise syntax, see other examples.

### We recommend to import Levers core like this to make your code less noisy
from levers import *

### Import one of the renderers you want to use
from levers.renderers import PyQtGraphRenderer
# from levers.renderers import PyGameRenderer


### The linkage description
p1 = Point(rotating(x=0, y=0, r=2, f=0.25))
p2 = Point(static(x=4, y=0))
c1 = Circle(center=p1, radius=5)
c2 = Circle(center=p2, radius=5)
p3 = Point(on_intersection(c1, c2, select=upper_left))
p4 = Point(on_line(p3, p1, -5))
p5 = Point(static(x=0, y=0))
Line(p1, p4)
Line(p2, p3)
Line(p1, p5)

### Different kinds of trails
Trail(p1, length=241)
Trail(
	p4, length=30, step=8,
	line_style=Style(width=1, color='#FF0000FF', visible=False),
	point_style=Style(width=4, color='#FF0000FF', visible=True),
)

### Render the animation using the renderer imported above
PyQtGraphRenderer(xmin=-4, xmax=11, ymin=-3, ymax=12, ppu=30).run(fps=60)
# PyGameRenderer(xmin=-4, xmax=11, ymin=-3, ymax=12, ppu=30).run(fps=60)

### Or capture the frames and save them to a folder
# PyQtGraphRenderer(-4, 11, -3, 12, 30).capture(fps=60, frames=240, path='capture_folder')
# PyGameRenderer(-4, 11, -3, 12, 30).capture(fps=60, frames=240, path='capture_folder')
