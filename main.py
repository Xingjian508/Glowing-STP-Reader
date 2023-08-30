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

  print('End of Test')
