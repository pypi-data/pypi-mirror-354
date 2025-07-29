# Levers
**Levers** is a Python package for visualizing lever mechanisms and animated geometry.  
It lets you describe a moving mechanism or geometric construction in just a few lines of code and visualize it using pluggable renderers.

<p align="center">
  <img src="media/demo2-1c.gif" width="400" alt="Chebyshev lambda linkage">
</p>

## Features

- Concise and natural syntax for describing mechanical linkages and geometry
- Optional rendering backends — choose what fits your use case
- No dependencies required for the core functionality

## Renderers and Installation

Although the project core has no external dependencies, vizualisation is performed via renderer plugins, each with its own requirements. You can choose optional dependencies at installation depending on the renderer you plan to use.

Currently, the package includes two renderer plugins:

- **PyGameRenderer** — install with:  
  ```bash
  pip install levers[pygame]
  ```
- **PyQtGraphRenderer** — install with:
  ```bash
  pip install levers[pyqt]
  ```
To install both:
```bash
pip install levers[all]
```

## Examples

Check the `examples/` folder to quickly learn how to use Levers!
