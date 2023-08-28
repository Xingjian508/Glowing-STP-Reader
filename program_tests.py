import unittest
from regular_obj import Vector, Edge, Plane, Bound, Face


class TestFaceContains1(unittest.TestCase):
  def setUp(self):
    c1, c2, c3 = (-10.0, 5.0, 3.0), (-10.0, -5.0, 3.0), (10.0, -5.0, 3.0)
    self.bound = Bound([Edge(c1, c2), Edge(c2, c3), Edge(c3, c1)])
    self.plane = Plane((0, 0, 3), (0, 0, 1))
    self.face = Face(plane=self.plane, bound=self.bound)

  def test_contains_outside(self):
    """Test a point that is outside the triangle formed by the vertices."""
    point_outside = Vector((0, 0, 0))
    self.assertFalse(self.face.contains(point_outside))


class TestFaceContains2(unittest.TestCase):
  def setUp(self):
    c1, c2, c3 = (0, 0, 0), (1, 0, 0), (0, 1, 0)
    self.bound = Bound([Edge(c1, c2), Edge(c2, c3), Edge(c3, c1)])
    self.plane = Plane((0, 0, 0), (0, 0, 1))
    self.face = Face(plane=self.plane, bound=self.bound)

  def test_contains_inside(self):
    """Test a point that is inside the triangle formed by the vertices."""
    point_inside = Vector((0.5, 0.5, 0))
    self.assertTrue(self.face.contains(point_inside))

  def test_contains_on_vertex(self):
    """Test a point that lies on a vertex of the triangle."""
    point_on_vertex = Vector((0, 0, 0))
    self.assertTrue(self.face.contains(point_on_vertex))

  def test_contains_outside(self):
    """Test a point that is outside the triangle formed by the vertices."""
    point_outside = Vector((1, 1, 0))
    self.assertFalse(self.face.contains(point_outside))


class TestFaceContains3(unittest.TestCase):
  def setUp(self):
    c1, c2, c3 = (-10.0, 5.0, 3.0), (-10.0, -5.0, 3.0), (10.0, -5.0, 3.0)
    self.bound = Bound([Edge(c1, c2), Edge(c2, c3), Edge(c3, c1)])
    self.plane = Plane((0, 0, 3), (0, 0, 1))
    self.face = Face(plane=self.plane, bound=self.bound)

  def test_contains_on_edge(self):
    """Test a point that lies on an edge of the triangle."""
    point_on_edge = Vector((-10.0, 0, 3.0))
    self.assertTrue(self.face.contains(point_on_edge))


class TestFaceContains4(unittest.TestCase):
  def setUp(self):
    c1, c2, c3 = (-10.0, 5.0, 3.0), (-10.0, -5.0, 3.0), (10.0, -5.0, 3.0)
    self.bound = Bound([Edge(c1, c2), Edge(c2, c3), Edge(c3, c1)])
    self.plane = Plane((0, 0, 3), (0, 0, 1))
    self.face = Face(plane=self.plane, bound=self.bound)

  def test_contains_inside_outside(self):
    """Test a point that is inside the triangle but outside the Plane."""
    point_inside_outside = Vector((-5.0, 0, 2.0))
    self.assertFalse(self.face.contains(point_inside_outside))


class TestFaceContains5(unittest.TestCase):
  def setUp(self):
    c1, c2, c3 = (-10.0, 5.0, 3.0), (-10.0, -5.0, 3.0), (10.0, -5.0, 3.0)
    self.bound = Bound([Edge(c1, c2), Edge(c2, c3), Edge(c3, c1)])
    self.plane = Plane((0, 0, 3), (0, 0, 1))
    self.face = Face(plane=self.plane, bound=self.bound)

  def test_contains_invalid_plane(self):
    """Test a point on a Plane with None location and axis."""
    point_invalid_plane = Vector((0, 0, 0))
    self.assertFalse(self.face.contains(point_invalid_plane))


class TestFaceContains6(unittest.TestCase):
  def setUp(self):
    c1, c2, c3 = (-10.0, 5.0, 3.0), (-10.0, -5.0, 3.0), (10.0, -5.0, 3.0)
    self.bound = Bound([Edge(c1, c2), Edge(c2, c3), Edge(c3, c1)])
    self.plane = Plane((0, 0, 3), (0, 0, 1))
    self.face = Face(plane=self.plane, bound=self.bound)

  def test_contains_origin(self):
    """Test the origin point that lies on the Plane."""
    point_origin = Vector((0, 0, 3))
    self.assertTrue(self.face.contains(point_origin))


if __name__ == "__main__":
  unittest.main()

