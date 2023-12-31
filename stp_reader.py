# Code Style:
# 1. All object attributes are shown in the __init__ methods.
# 2. All helper methods "_func()" are front-underscored and are static methods.
# 3. All dunder "__func__()" are defined first, then the helpers, then the rest.
# 4. All classes and methods, including dunders and helpers, have docstrings.
# 5. All objects can be created without default parameters.
# 6. Use 2 spaces for a tab, 2 lines for level 1, and 1 line for level 2.


# TODO: Finish up the utilization of "shadow", according to program features in the user manual.
# TODO: Examine why this simple counter thing has a problem.

from steptools import step
from regular_obj import Config, Face, Bound, Plane, Edge, Vector
from nonregular_obj import ToroidalFace


def approx(tup) -> tuple:
  """Returns approximated values for tuples."""
  return tuple(round(e, Config.DECIMALS) for e in tup)


def approx_vec(vec) -> tuple:
  """Returns approximated values for Vectors."""
  return Vector(approx(vec.coordinates))


def withdividers(func):
  """Decorator to help print dividers."""
  def new_line_added_func(*args):
    print()
    print('******')
    func(*args)
    print('******')
    print()
  return new_line_added_func


@withdividers
def display_all_objects(objects):
  """Displays all objects."""
  for key in objects:
    print(f'Object "{key}":')
    for obj in objects[key]:
      print(obj)
    print('------')


class STPFile:
  """Stores an STP file."""
  def __init__(self, file_path=None):
    """Initializes an STPFile object."""
    if file_path is not None:
      self.stp_file = step.open_project(file_path)
    self.unreadable = []
    self.unreadable_types = set()
    self.face_types = dict()

  def __repr__(self):
    """Returns the string representation."""
    return f'STPFile({file_path})'

  def _count_face_type(self, face_obj):
    """Counts the face type."""
    if step.type(face_obj) == 'advanced_face':
      k = step.type(face_obj.face_geometry)
      if k in self.face_types:
        self.face_types[k] += 1
      else:
        self.face_types[k] = 1

  def _convert(self, obj):
    """Converts an stp object to a self defined one."""
    def pt_tup(cartesian_point_obj) -> tuple:
      return approx(tuple(cartesian_point_obj.coordinates))
    
    def vec_tup(direction_obj) -> tuple:
      return approx(tuple(direction_obj.direction_ratios))
  
    def get_pos_attr(pos) -> tuple:
      loc, ax, ref_d = pos.location, pos.axis, pos.ref_direction
      return (pt_tup(loc), vec_tup(ax), vec_tup(ref_d))

    def get_plane_attr(face_obj) -> tuple:
      pos = face_obj.face_geometry.position
      return get_pos_attr(pos)

    def get_face_edges(face_obj) -> list:
      e_list = face_obj.bounds[0].bound.edge_list
      edges = []
      for edge in e_list:
        v_s = edge.edge_element.edge_start.vertex_geometry
        v_e = edge.edge_element.edge_end.vertex_geometry
        edges.append(Edge(pt_tup(v_s), pt_tup(v_e)))
      return edges

    def get_tor_edges(face_obj):
      e = face_obj.bounds[0].bound.edge_list[0].edge_element

      v_s = e.edge_start.vertex_geometry
      v_e = e.edge_end.vertex_geometry
      eg = e.edge_geometry

      plane = Plane(*get_pos_attr(eg.position))
      edge = Edge(pt_tup(v_s), pt_tup(v_e))
      return edge, plane
      
    def create_face(obj):
      fg = step.type(obj.face_geometry)
      if fg == 'plane':
        bound = Bound(get_face_edges(obj))
        plane = Plane(*get_plane_attr(obj))
        return Face(plane, bound)
      elif fg == 'toroidal_surface':
        edge, plane = get_tor_edges(obj)
        maj_r, min_r = fg.major_radius, fg.minor_radius
        return ToroidalFace(plane, edge, maj_r, min_r)
      else:
        raise Exception('Cannot be created.')
    
    if step.type(obj) == 'advanced_face':
      return create_face(obj)

    if step.type(obj) == 'vertex_point':
      pt_geometry = obj.vertex_geometry
      return Vector(pt_tup(pt_geometry))
  
    return None

  @withdividers
  def print_face_stats(self):
    """Prints how many faces are of each type."""
    for key in self.face_types:
      print(f'{key}: {self.face_types[key]}')

  def print_errors(self):
    """Prints all objects that had error being read."""
    if len(self.unreadable):
      print(f'- Out of all faces, {len(self.unreadable)} are '+
          f'unreadable, with formats {self.unreadable_types}.') 
    else:
      print('All faces are readable.')

  def get_3D_objects(self, types=None):
    """Returns the 3D objects in the file."""
    keys = set(types)
    objects = {key: [] for key in keys}

    for obj in step.DesignCursor(self.stp_file):
      if step.type(obj) in keys and len(keys):
        self._count_face_type(obj)
        try:
          objects[step.type(obj)].append(self._convert(obj))
        except Exception as e:
          self.unreadable.append(obj)
          self.unreadable_types.add(step.type(obj.face_geometry))

    return objects


class PlaneCollection:
  """Stores planes."""
  def __init__(self, planes=None):
    """Initializes a PlaneCollection object."""
    self.planes = planes
    self.parallel = self._make_parallel(planes)
    self._sort_by_axis_pos(self.parallel)

  def __repr__(self):
    """Returns the string representation."""
    return f'PlaneCollection({str(self.planes)})'

  @staticmethod
  def _make_parallel(planes: list):
    """Returns a dictionary of planes sorted by axis."""
    parallel = dict()
    for plane in planes:
      abs_unit_ax = approx_vec(plane.abs_unit_dir())
      if abs_unit_ax in parallel:
        parallel[abs_unit_ax].append(plane)
      else:
        parallel[abs_unit_ax] = [plane]
    return parallel

  @staticmethod
  def _sort_by_axis_pos(planes_by_dir: dict):
    """Sorts values (in plane lists) by axis positions."""
    for key in planes_by_dir:
      planes = planes_by_dir[key]
      planes_by_dir[key] = sorted(planes, key=lambda p:\
                                  p.pos_from_origin())

  @withdividers
  def display_planes(self):
    """Prints out each direction and its planes."""
    for direction in self.parallel:
      print(f'Direction: {direction.coordinates}')
      for plane in self.parallel[direction]:
        print(f'Position {plane.pos_from_origin()}, {plane}')
      print('------')
  
  @withdividers
  def display_pairwise_distances(self):
    """Prints out each two planes' distance."""
    for direction in self.parallel:
      col = self.parallel[direction]
      print(f'At direction {direction}:')
      for i in range(len(self.parallel[direction])-1):
        print(f'Plane {i} and Plane {i+1} distance:', \
              f'{col[i].distance_to_plane(col[i+1])}')
      total = len(self.parallel[direction])-1
      print(f'Plane 0 and Plane {total} distance:', \
            f'{col[0].distance_to_plane(col[total])}')
      print('------')


class FaceCollection:
  """Stores faces."""
  def __init__(self, faces=None):
    """Initializes a FaceCollection object."""
    self.faces = faces
    self.parallel = self._make_parallel(faces)
    self._sort_by_axis_pos(self.parallel)

  def __repr__(self):
    """Returns the string representation."""
    return f'FaceCollection({str(self.faces)})'

  def __len__(self):
    """Returns the length of faces."""
    return len(self.faces)

  @staticmethod
  def _make_parallel(faces: list):
    """Returns a dictionary of faces sorted by axis."""
    parallel = dict()
    for face in faces:
      abs_unit_ax = approx_vec(face.plane.abs_unit_dir())
      if abs_unit_ax in parallel:
        parallel[abs_unit_ax].append(face)
      else:
        parallel[abs_unit_ax] = [face]
    return parallel

  @staticmethod
  def _sort_by_axis_pos(faces_by_dir: dict):
    """Sorts values (in face lists) by axis positions."""
    for key in faces_by_dir:
      faces = faces_by_dir[key]
      faces_by_dir[key] = sorted(faces, key=lambda f:\
                                  f.plane.pos_from_origin())

  @withdividers
  def display_faces(self):
    """Prints out each direction and its planes."""
    for direction in self.parallel:
      print(f'Direction: {direction.coordinates}')
      for face in self.parallel[direction]:
        print(f'Position {face.plane.pos_from_origin()}, {face}')
      print('------')

  @withdividers
  def display_pairwise_shadowing(self):
    """Prints out the pairwise shadowing status."""
    for direction in self.parallel:
      print(f'Direction: {direction.coordinates}')
      face_list = self.parallel[direction]
      for i in range(len(face_list)-1):
        print(face_list[i])
        print(face_list[i+1])
        print(face_list[i].shadow(face_list[i+1]))
        print()
      print()
  

# ------Execution below.------


def main(precision, path, types, out=True):
  """Executes the parallel-finding program."""
  # Setting up.
  Config.DECIMALS = precision
  design = STPFile(path)

  # Gets the self-defined objects by type.
  objects = design.get_3D_objects(types)

  # Gets the planes and categorize by parallel.
  face_list = objects['advanced_face']
  faces = FaceCollection([f for f in face_list if type(f) == Face])
  
  # # NOTE: now here are three things we can do.

  # 1. Displays all objects.
  # display_all_objects(objects)

  # 2. Displays the planes.
  # faces.display_faces()

  # 3. Displays the pairwise distances.
  # planes.display_pairwise_distances()

  # 4. Displays pairwise shadowing.
  # faces.display_pairwise_shadowing()

  # Displaying read results when requested.
  if out:
    design.print_face_stats()
    design.print_errors()
    print(f"- Successfully read {len(faces)} faces.")

