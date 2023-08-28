from stp_reader import main


if __name__ == '__main__':
  # Setting up.
  PRECISION = 2
  PATH = 'surface.stp'
  TYPES = 'advanced_face', 'vertex_point'
  
  # Executes the program.
  main(PRECISION, PATH, TYPES)

