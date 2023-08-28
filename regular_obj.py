import math


class Config:
  """Stores necesssary configurations."""
  # NOTE! DECIMALS by default, unless changed.
  DECIMALS = 3


class Vector:
  """Stores a 3D point."""
  def __init__(self, c=None):
    """Initializes a Vector object."""
    self.x, self.y, self.z = self._init_xyz(c)
    self.coordinates = (self.x, self.y, self.z)

  @staticmethod
  def _init_xyz(c):
    """Initializes the x, y, z if c is valid."""
    if isinstance(c, tuple) and len(c) == 3:
      return tuple(n if not n==0 else 0 for n in c)
    return None, None, None

  def __repr__(self):
    """Returns the string representation."""
    return f'Vector({self.x}, {self.y}, {self.z})'
  
  def __iter__(self):
    """Turning the object iterable."""
    for vi in self.coordinates:
      yield vi

  def __hash__(self):
    """Custom hash function based on coordinates."""
    return hash(self.coordinates)

  def __eq__(self, other):
    """Checks if two vectors are equal."""
    for c1, c2 in zip(self.coordinates, other.coordinates):
      if abs(c1-c2) > (1/math.pow(10, Config.DECIMALS)):
        return False
    return True

  def __add__(self, other):
    """Adds two Vector objects."""
    return Vector((self.x+other.x, self.y+other.y, self.z+other.z))

  def __sub__(self, other):
    """Subtracts two Vector objects."""
    return Vector((self.x-other.x, self.y-other.y, self.z-other.z))

  def __mul__(self, scalar):
    """Performs left-hand scalar multiplication."""
    scaled_coordinates = (scalar * self.x, scalar * self.y, scalar * self.z)
    return Vector(scaled_coordinates)

  def __rmul__(self, scalar):
    """Performs right-hand scalar multiplication."""
    return self * scalar

  def distance_to_point(self, v):
    """Calculates the distance between self and v."""
    dx = (self.x-v.x)*(self.x-v.x)
    dy = (self.y-v.y)*(self.y-v.y)
    dz = (self.z-v.z)*(self.z-v.z)
    return math.sqrt(dx+dy+dz)

  def dot_product(self, other):
    """Calculates the dot product."""
    return self.x*other.x + self.y*other.y + self.z*other.z

  def cross_product(self, other):
    """Calculates the cross product."""
    cross_x = self.y*other.z - self.z*other.y
    cross_y = self.z*other.x - self.x*other.z
    cross_z = self.x*other.y - self.y*other.x
    return Vector((cross_x, cross_y, cross_z))

  def norm(self):
    """Calculates the norm of the vector."""
    return self.distance_to_point(Vector((0, 0, 0)))

  def unit(self):
    """Returns the unit vector."""
    return self*(1/self.norm())


class Edge:
  """Stores two 3D points."""
  def __init__(self, start=None, end=None):
    """Initializes an Edge object."""
    self.start = Vector(start)
    self.end = Vector(end)

  def __repr__(self):
    """Returns the string representation."""
    s, t = self.start.coordinates, self.end.coordinates
    return f'Edge({s}, {t})'


class Plane:
  """Stores two vectors."""
  def __init__(self, loc=None, ax=None, ref_d=None):
    """Initializes a Plane object."""
    self.location = Vector(loc)
    self.axis = Vector(ax)
    self.ref_direction = ref_d

  def __repr__(self):
    """Returns the string representation."""
    loc, ax = self.location.coordinates, self.axis.coordinates
    return f'Plane(anchor={loc}, normal={ax})'

  def __eq__(self, other):
    """Checks if two planes are equal."""
    loc_eq = self.location == other.location
    ax_eq = self.axis == other.axis
    ref_eq = self.ref_direction == other.ref_direction
    return loc_eq and ax_eq and ref_eq

  def nonempty(self):
    """Determines if the self object is empty."""
    return self.location is not None and self.axis is not None

  def contains(self, v):
    """Determines if the Vector v is on the plane."""
    dot_perp = (v-self.location).dot_product(self.axis)
    return dot_perp <= 1/(math.pow(10, Config.DECIMALS)) and self.nonempty()

  def is_parallel_to(self, other):
    """Determines if the Plane p is parallel to this plane."""
    return self.abs_unit_dir() == other.abs_unit_dir() and self.nonempty()

  def abs_unit_dir(self):
    """Returns the absolute unit direction of the plane."""
    # Note: the first non-zero value must be positive.
    ax_dir = self.axis.unit()
    for k in ax_dir:
      if k > 0:
        return ax_dir
      elif k < 0:
        return (-1) * ax_dir
    return ax_dir

  def distance_to_plane(self, other):
    """Calculates the distance between parallel planes."""
    if self.is_parallel_to(other):
      distance = abs((other.location-self.location).dot_product(self.axis.unit()))
      return distance
    else:
      raise ValueError('Distance between planes exists iff parallel!')

  def distance_to_point(self, v):
    """Calculates the distance to point v."""
    return abs((v-self.location).dot_product(self.axis.unit()))

  def pos_from_origin(self, origin=Vector((0, 0, 0))):
    """Calculates the position from zero, unless otherwise stated."""
    dist_from_origin = self.distance_to_point(origin)
    # Note: it is necessary to check whether the direction is the opposite.
    if self.contains(self.abs_unit_dir()*dist_from_origin):
      return dist_from_origin
    elif self.contains((-1)*self.abs_unit_dir()*dist_from_origin):
      return -dist_from_origin
    else:
      raise ValueError("Makes no sense. The plane has no pos from origin.")


class Bound:
  """Stores a collection of edges."""
  def __init__(self, edges=None):
    """Initializes a Bound object."""
    self.edges = edges
    self.vertices = self._connect(edges)

  def __iter__(self):
    """Iterator method for Bound object."""
    for edge in self.edges:
      yield edge

  @staticmethod
  def _connect(edges):
    """Connects the edges."""
    con = dict()
    used = set()
    for edge in edges:
      if edge.start not in con:
        con[edge.start] = edge.end
      else:
        assert edge.end not in con
        con[edge.end] = edge.start
    return con

  def get_loop(self, start_pos=None):
    """Returns a loop that describes the bound."""
    output = []

    key = next(iter(self.vertices))
    while len(output) < len(self.vertices):
      output.append(self.vertices[key])
      key = self.vertices[key]
    return output

  def print_loop(self, start_pos=None):
    """Prints out the loop in node format."""
    output = ""
    vert_list = self.get_loop(start_pos)
    for vert in vert_list:
      output += str(vert) + ' <-> '
    output += 'origin'
    print(output)


class Face:
  """Stores a Plane and Bound object."""
  def __init__(self, plane=None, bound=None):
    """Initializes a Face object."""
    self.plane = plane
    self.bound = bound

  def __repr__(self):
    """Returns the string representation."""
    output = f'Face(\n  {self.plane}\n'
    for edge in self.bound:
      output += '  ' + str(edge) + '\n'
    output += ')'
    return output

  @staticmethod
  def _tri_area(v1, v2, v3):
    """Returns the triangular area inscribed in three Vector objects."""
    v, u = v2-v1, v3-v1
    return v.cross_product(u).norm()/2.0

  @staticmethod
  def _tri_contains(p, v1, v2, v3):
    """Determines whether the point lies in the triangle inscribed."""
    total_area = Face._tri_area(v1, v2, v3)
    t_sum = Face._tri_area(p, v1, v2) + \
            Face._tri_area(p, v2, v3) + \
            Face._tri_area(p, v3, v1)
    return abs(total_area-t_sum) < (1/math.pow(10, Config.DECIMALS))

  def area(self):
    """Returns the total area of the Face object."""
    verts = self.bound.get_loop()
    pivot = verts[0]
    
    total_area = 0
    for i in range(1, len(verts)-1):
      total_area += self._tri_area(pivot, verts[i], verts[i+1])
    return total_area

  def contains(self, v):
    """Determines if v rests on the Face object."""
    if self.plane.contains(v):
      verts = self.bound.get_loop()
      pivot = verts[0]
      for i in range(1, len(verts)-1):
        if self._tri_contains(v, pivot, verts[i], verts[i+1]):
          return True
    return False

