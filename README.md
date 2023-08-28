# Parallel Plane Analyzer for STEP Files

HI EVERYONE! I wrote this program that allows us to analyze and explore objects within STEP files. It uses the `steptools` library for working with STEP files, while enabling us to extract, categorize, and do numerical operations with 3D objects taken from the file.

## Features

- Extracts 3D objects from STEP files and categorizes them by type.
- Processes and converts STEP objects into user-defined classes for enhanced functionality.
- Constructs planes and categorizes them based on parallel directions.
- Provides tools to display plane information, including positions, directions, and distances.
- Demonstrates how to use self-defined classes for 3D geometry operations.

## Requirements

- Python 3
- `steptools` library (for working with STEP files)

## Usage

1. Clone the repository and navigate to the project directory.

2. Modify the `main` function in the provided code to specify your desired precision, path to the STEP file, and object types you want to analyze.

3. Run the program using `python3 main.py` in the terminal.

4. Observe the output, which displays information about extracted objects, categorized planes, and pairwise distances.

## Custom Classes

The program defines several custom classes for working with 3D geometry, including `Vector`, `Edge`, `Bound`, and more. These classes provide fundamental operations for vectors, edges, surfaces, and geometric transformations.

## Contributing

Contributions, suggestions, and improvements are welcome! Feel free to open issues or submit pull requests.

## License

Just me lol.

---

Created by Xingjian Wang, August 2023
