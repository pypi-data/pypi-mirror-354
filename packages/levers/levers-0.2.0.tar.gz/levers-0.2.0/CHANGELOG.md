# Changelog

## v0.1.0 - 2025-06-05
The first version of Levers
### Added
- geometry: Point, Line, Circle, Trail, and Style for all of them
- motions: static, rotating, on_intersection, on_line
- selectors: 
  - 8 absolute selectors (lower_left, lower_right, etc.)
  - 4 relative selectors (closest_to, furthest_from, most_clockwise_from, most_counterclockwise_from)
- renderers: PyQtGraphRenderer, PyGameRenderer
- examples: 
  - demo1 - Custom mechanism
  - demo2 - Chebyshev lambda linkage

## v0.2.0 - 2025-06-09
### Added
- motions: on_angle_side, sliding
- examples: demo3 - Chebyshev long-dwell linkage
### Changed
- Trail now has line and point components with independent configuration, coordinate saving frequency is now configurable. Both renderers updated to support this.
- Improved explanation in all the example files
