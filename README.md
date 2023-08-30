# Parallel Plane Analyzer for STEP Files

HI EVERYONE! I wrote this program that allows us to analyze and explore objects within STEP files. It uses the `steptools` library for working with STEP files, while enabling us to extract, categorize, and do numerical operations with 3D objects taken from the file.

## Features

- Extracts 3D objects from STEP files and categorizes them by type.
- Processes and converts STEP objects into user-defined classes for enhanced functionality.
- Constructs planes and categorizes them based on parallel directions.
- Provides tools to display plane information, including positions, directions, and distances.
- Has self-defined classes for 3D geometry operations.

## Requirements

- Python 3
- `steptools` library (for working with STEP files)

## Custom Classes

The program defines several custom classes for working with 3D geometry, including `Vector`, `Edge`, `Bound`, and more. These classes provide fundamental operations for vectors, edges, surfaces, and geometric transformations.

### Progress (As of August 30th)
- Ran 8 STP test files through the program. I did not upload them as the STP designs are not owned by me. However, the code had read all planar surfaces, while printing faces of curved surfaces (I haven't figured out how to read a curved surface yet, might require some non-linear equations).
- **I consider it quite successful; the program can read planes from all STP files**. Printout is provided below (code block 1). Also wrote unit tests and did debugging.

### Short-Term Goals
- ***Create a user manual for the developed program, add comments to each part for future maintenance and continuation of work.***
- ***Compile the computable data, provide conceptual definitions. Here are features already accomplished:***
    1. Sorting planes along an axis.
       - An "axis" is a line passing through the origin in 3D space. Given $n$ planes, let $P = \{p_1, p_2, ...\}$ such that $p_i$ represents the position of the $i$-th plane on this axis ($p_i \in \mathbb{R}$). Then:
       - **We can calculate the minimum distance $\min|p_{i}-p_{i+1}| \text{, for all } p_i, p_{i+1} \in P$ to obtain the smallest separation between two parallel planes. This can also represent "thickness" of a slab.** Customizable level of approximation.
    2. Displaying the outer "edges" of the planes. An "edge" is defined as $(v_i, v_j) \text{ where } v_i, v_j$ are two vertices (or vectors, identically represented). This program can verify and print the cycle of edges, i.e., output $\{(v_1, v_2), (v_2, v_3), ..., (v_n, v_1)\}$, **which forms the outer "edge"**.

### Future Code Maintenance
1. **Thickness Calculation**: Instead of solely relying on distance between planes, "thickness" can be inferred by checking whether two parallel faces "cover" each other on the same axis. It's also possible to check for the existence of other parallel planes connected by edges between the two planes.
    - Consider a can. The top and bottom of the can are two parallel planes, and there are also side surfaces connecting the outer "edge" of the top and bottom. In this scenario, it's considered to have "thickness".
    - **Building upon the existing program, this isn't overly complex**. If successful hashing is available, it would take $\mathbf{O}(n)$ time.
2. **Calculating Rib Height, Width, Draft Angle**: My conclusion regarding this matter is that while using AI could be attempted, a well-defined convention (when does an object have "height, width, draft angle") would be more straightforward. For example, for objects with certain attributes, a correct calculation can be achieved. Some flexibility can be allowed, but with precise definitions (height being the tallest "rod," a "rod" being approximately four-sided with an aspect ratio greater than n units...), it might work better.

## Contributing

Contributions, suggestions, and improvements are welcome! Feel free to open issues or submit pull requests.

## License

Just me lol.

---

Created by Xingjian Wang, August 2023

**Code Block 1**
``` python
Start of Test

Test: test1.stp
- Out of all faces, 4 are unreadable, with formats {'b_spline_surface_with_knots'}.
- Successfully read 14 faces.

Test: test2.stp
- Out of all faces, 9 are unreadable, with formats {'b_spline_surface_with_knots_and_rational_b_spline_surface', 'b_spline_surface_with_knots'}.
- Successfully read 8 faces.

Test: test3.stp
- Out of all faces, 11 are unreadable, with formats {'b_spline_surface_with_knots_and_rational_b_spline_surface', 'b_spline_surface_with_knots'}.
- Successfully read 8 faces.

Test: test4.stp
- Out of all faces, 16 are unreadable, with formats {'b_spline_surface_with_knots_and_rational_b_spline_surface', 'b_spline_surface_with_knots'}.
- Successfully read 8 faces.

Test: sample_surface.stp
- Out of all faces, 16 are unreadable, with formats {'b_spline_surface_with_knots_and_rational_b_spline_surface', 'b_spline_surface_with_knots'}.
- Successfully read 12 faces.

Test: hard.stp
- Out of all faces, 42 are unreadable, with formats {'toroidal_surface', 'b_spline_surface_with_knots_and_rational_b_spline_surface', 'b_spline_surface_with_knots'}.
- Successfully read 276 faces.

Test: hud_shell.stp
- Out of all faces, 117 are unreadable, with formats {'surface_of_linear_extrusion', 'toroidal_surface', 'b_spline_surface_with_knots_and_rational_b_spline_surface', 'b_spline_surface_with_knots'}.
- Successfully read 625 faces.

Test: surface.stp
- Out of all faces, 120 are unreadable, with formats {'surface_of_linear_extrusion', 'toroidal_surface', 'b_spline_surface_with_knots_and_rational_b_spline_surface', 'b_spline_surface_with_knots'}.
- Successfully read 5 faces.

End of Test
```
