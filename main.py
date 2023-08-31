# Code Style:
# 1. All object attributes are shown in the __init__ methods.
# 2. All helper methods "_func()" are front-underscored and are static methods.
# 3. All dunder "__func__()" are defined first, then the helpers, then the rest.
# 4. All classes and methods, including dunders and helpers, have docstrings.
# 5. All objects can be created without default parameters.
# 6. Use 2 spaces for a tab, 2 lines for level 1, and 1 line for level 2.


from stp_reader import main


if __name__ == '__main__':
  # Setting up.
  PRECISION = 3
  PATHS = ['sample_surface.stp', 'hard.stp', 'hud_shell.stp', 'surface.stp']
  TYPES = 'advanced_face', 'vertex_point'
  
  # Executes the program.
  main(PRECISION, f'stp_files/sample_surface.stp', TYPES, out=False)
  print('Start of Test')

  # NOTE: TEST with test bundle.
  for i in range(1, 5):
    print(f'Test: test{i}.stp')
    main(PRECISION, f'stp_files/test{i}.stp', TYPES)
    print()

  # NOTE: TEST with real life projects.
  for PATH in PATHS:
    print(f'Test: {PATH}')
    main(PRECISION, f'stp_files/{PATH}', TYPES)
    print()
