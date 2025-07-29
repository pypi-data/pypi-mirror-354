def __getattr__(name):
	if name == "PyQtGraphRenderer":
		from .pyqtgraph_renderer import PyQtGraphRenderer
		return PyQtGraphRenderer
	if name == "PyGameRenderer":
		from .pygame_renderer import PyGameRenderer
		return PyGameRenderer

__all__ = ["PyQtGraphRenderer", "PyGameRenderer"]
