### This is a custom example to demonstrate some of the capabilities of Levers.
### In this file, we avoid using keyword arguments unnecessarily.

### We recommend to import Levers core like this to make your code less noisy
from levers import *

### Import one of the renderers you want to use
from levers.renderers import PyQtGraphRenderer
# from levers.renderers import PyGameRenderer

### Pre-define styles for some objects 
red_point = Style(visible=True, color='#FF0000FF', width=10)
green_line = Style(visible=True, color='#00AA00FF', width=1)

### Common part of the mechanism
p2 = Point(static(2, 2), style=red_point)
p4 = Point(static(7, 2), style=red_point)

### Blue part of mechanism
### Notice how we use invisible circles to describe the motion of a flying point
p1 = Point(rotating(2, 2, 1.5, 0.25))
Line(p1, p2)
c1 = Circle(p1, 4)
c2 = Circle(p4, 3)
p5 = Point(on_intersection(c1, c2))
Line(p1, p5)
Line(p5, p4)

### Green part of the mechanism
p3 = Point(on_line(p2, p1, -0.7))
Line(p2, p3, style=green_line)
p6 = Point(on_line(p3, p4, 6))
Line(p3, p6, style=green_line)

### Render the animation using the renderer imported above
PyQtGraphRenderer(0, 9, -2, 5, 60).run(60)
# PyGameRenderer(0, 9, -2, 5, 60).run(60)

### Or capture the frames and save them to a folder
# PyQtGraphRenderer(0, 9, -2, 5, 80).capture(60, 120, 'capture_folder')
# PyGameRenderer(0, 9, -2, 5, 80).capture(60, 120, 'capture_folder')
