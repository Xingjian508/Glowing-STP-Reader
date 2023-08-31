# Surface Analyzer for STP Files

HI EVERYONE! I wrote this program that allows us to analyze and explore 3D objects within STP files. It uses the `steptools` library for working with STP files, while enabling us to extract, categorize, and do numerical operations with 3D objects taken from the file.

### Definitions
> The program is object oriented; it mimics the idea of these 3D objects in reality. Here are definitions for each and their design decisions.
- **Vector/Vertex**: a vector $v$ is a collection of $(x, y, z)$ points in the $\mathbb{R}^3$ space.
	- It could be interpreted as an "arrow with direction and magnitude", or a "point" in a 3D space (which means vertex).
- **Edge**: an edge $e$ is a tuple of $2$ vectors $(v_{\text{start}}, v_{\text{end}})$ representing an edge segment.
- **Graph**: a graph $G$ contains $V$ and $E$.
	- $V$ is the collection of vertices $\\{v_1, v_2, ..., v_n\\}$.
	- $E$ is the collection of edges. $E \subset V \times V$, with $v_i \neq v_j$ for any $(v_i, v_j) \in E$.
- **Bound**: a bound $B$ is a circular graph with $n$ vertices and $n$ edges.
	- Its edges $E$ is strictly a cycle, with $E = \\{(v_1, v_2), (v_2, v_3), ..., (v_n, v_1)\\}$.
- **Plane**: a plane $P$ is represented by two vectors $v_{\text{anchor}}$ and $v_{\text{normal}}$.
	 - Interpretation: the plane "starts" at $v_{\text{anchor}}$, and faces the $v_{\text{normal}}$ direction.
	 - Formally, we can define $P = \\{\alpha v_p + v_{\text{anchor}} : \forall \alpha \in \mathbb{R}, \forall v_p \cdot v_{\text{normal}} = 0\\}$.
- **Face**: a face $F$ contains a bound $B$ and a plane $P$.

### Program Features
1. Reading all STP `advanced_faces` and converting them to `Face` objects.
	- Encapsulates the `Plane` they are on, and the `Bound` they reside in.
	- Requires these faces to be planar, not curved.
2. Grouping the parallel `Face` together.
	- Creates, for each $v_{\text{normal}}$, an array of faces with the same normal vector.
	- Constructs mapping between $v \rightarrow \text{array} \langle F \rangle$.
3. Sorting `Plane` by their position on the same axis.
	- Any axis in the 3D plane works, representing the planes' normal vectors.
	- Find the axis-position of plane $P_i$ denoted as $p_i \in \mathbb{R}$. Sort planes by $p_i$.
4. Displaying pairwise `Plane` distances.
	- For sorted $\text{array}\langle P \rangle$ of length $n$ described above, the distance between consecutive $P_i$ and $P_{i+1}$ can be calculated.
	- Moreover, $\min|p_{i}-p_{i+1}| \text{ for all } i < n$ yields a lower bound for the thickness of any "slab".
1. Calculating the area of each `Face`.
	- Any number of edges is fine — the classic polygon area problem.
2. Detecting if `Face` overlap with each other.
	- For two faces $F_1, F_2$, they overlap each other when, on the same axis, one can "project a shadow" onto the other.
	- A formal definition would be that there exists points $p_1 \in F_1, p_2 \in F_2$ such that the edge $(p_1, p_2)$ is perpendicular to both $F_1$ and $F_2$.

### Program Structure
- `main.py` runs the program. Three configurations are needed.
	- `PRECISION: int` (the number of decimals desired).
	- `PATH: str` (the path of the STP file).
	- `TYPES: tuple` (the types of objects we wish to extract).
- `stp_reader.py` stores the functions necessary to interpret STP files and initialize our custom 3D objects.
	- The `main` function has detailed instructions on usable commands.
	- The `STPFile` object stores an STP file, and returns a list of custom defined 3D objects. `PlaneCollection` processes them (e.g. `make_parallel`).
	- At the end, unreadable faces (curved surfaces) are printed.
- `regular_obj.py` stores all the aforementioned 3D objects.
	- `Vector` can add, subtract, scalar multiplication, calculate norm, unit vector, and dot & cross products. It can also be iterated and hashed.
	- `Edge` is just two `Vector` objects.
	- `Plane` can check if it contains a `Vector`, return its unit normal vector, check if it is parallel with another plane (and if so, calculate the distance in between), calculate if it contains a point, calculate the distance to a point, calculate its position from origin.
	- `Bound` checks if the inputted edges form a strict loop, and connects the loop using a dictionary, storing a sorted edge list.
	- `Face` can calculate its area, and whether it contains a point.
- `program_tests.py` provides unit testing for the `regular_obj.py` file.

### Usage & Prerequisites
The usage of the program is labeled in the code, in detail. The prerequisites needed include Python3, and `steptools`.

### Code Maintenance and Improvement Ideas
1. **Enhance Thickness Calculation Method**: Instead of relying solely on distance, consider whether two parallel planes overlap each other on the same axis to determine their thickness (mentioned in "Program Features"). One can also examine the existence of other parallel planes and connect their "edges".
	- For example, think of a can: the top and bottom are two parallel planes, and there's a side connecting the outer "edges" of both the top and bottom. In this scenario, we say there's "thickness".
	- **This isn't difficult to implement on top of the existing program**. With a successful hash, it would only require $\text{O}(n)$ time complexity.
2. **Calculate "Rib" Height, Width, and Draft Angle**: Having a well-defined convention (defining when an object has "height, width, draft angle") would be more straightforward. For instance, in the attached image below, precise definition (where height is the highest point of a "rib," a "rib" is approximately four-sided with an aspect ratio exceeding n units) could be more beneficial.
---

Created by Xingjian Wang, August 2023

**Code Block 1 - Testing Results**
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
