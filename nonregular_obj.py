# Code Style:
# 1. All object attributes are shown in the __init__ methods.
# 2. All helper methods "_func()" are front-underscored and are static methods.
# 3. All dunder "__func__()" are defined first, then the helpers, then the rest.
# 4. All classes and methods, including dunders and helpers, have docstrings.
# 5. All objects can be created without default parameters.
# 6. Use 2 spaces for a tab, 2 lines for level 1, and 1 line for level 2.


import math
from regular_obj import Plane


class Circle:
  """Stores a Circle object."""
  def __init__(self, rad, plane):
    self.radius = rad
    self.plane = plane


class ToroidalFace:
  """Stores a ToroidalFace object."""
  def __init__(self, plane, edge, maj_r, min_r):
    self.plane = plane
    self.edge = edge
    self.major_radius = maj_r
    self.minor_radius = min_r


def do_something():
  e_list = face_obj.bounds[0].bound.edge_list
  edges = []
  for edge in e_list:
    v_s = edge.edge_element.edge_start.vertex_geometry
    v_e = edge.edge_element.edge_end.vertex_geometry
    eg = edge.edge_element.edge_geometry
    # Now eg is a circle with radius and position (plane).
