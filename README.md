*This project has been created as part of the 42 curriculum by fgoncal2, misousa*

# A-Maze-ing

## Description
A-Maze-ing is a maze generator and solver written in Python.

Given a configuration file, the program:
- builds a maze of the requested size (optionally a *perfect* maze — one with
  exactly one path between any two cells),
- writes the maze to an output file using a compact hexadecimal wall encoding,
- computes the shortest path between the entry and the exit,
- displays the maze in the terminal, with an interactive loop to regenerate it,
  toggle the solution path, and change the wall colours.

The maze generation logic lives in a standalone, reusable module (`mazegen`)
that is packaged as a `pip`-installable wheel so it can be imported by other
projects.

## Instructions

### Requirements
- Python 3.10 or newer.
- A virtual environment is recommended:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Running the project
From the repository root:
```bash
make run                          # uses config.txt
python3 a_maze_ing.py config.txt  # or run directly with any config file
```
This generates the maze, writes the hex-encoded output file (the path set by
`OUTPUT_FILE` in the config), computes the shortest path, and launches the
interactive visualiser.

### Building the reusable package from source
The `mazegen` package is built from the sources in this repository with the
standard Python build tooling:
```bash
pip install build      # build front-end (one-time)
python3 -m build       # produces dist/mazegen-1.0.0-py3-none-any.whl (and .tar.gz)
```
A built wheel is also committed at the repository root
(`mazegen-1.0.0-py3-none-any.whl`).

### Installing the package
To reuse the generator in another project, install the wheel into any
environment:
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```
Then `from mazegen import MazeGenerator` — see the **Reusable module** section
below for usage.

### Development (linting)
```bash
make install        # installs flake8 + mypy
make lint           # flake8 + mypy
make lint-strict    # flake8 + mypy --strict
```

## Config file format
The configuration is a plain text file of `KEY=VALUE` lines. Blank lines and
lines starting with `#` are ignored. Each key may appear only once; unknown
keys are rejected.

| Key | Type | Required | Meaning |
|-----|------|----------|---------|
| `WIDTH` | integer > 0 | yes | Number of columns. |
| `HEIGHT` | integer > 0 | yes | Number of rows. |
| `ENTRY` | `x,y` | yes | Entry cell. `x` = column (0 = left), `y` = row (0 = top). |
| `EXIT` | `x,y` | yes | Exit cell, in bounds and distinct from the entry. |
| `OUTPUT_FILE` | filename | yes | Where the encoded maze is written. |
| `PERFECT` | `True` / `False` | yes | `True` = perfect maze; `False` = extra loops added. |
| `SEED` | integer | no | Fixes the RNG for reproducible mazes. Omit for random. |

Example (`config.txt`):
```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## The maze generation algorithm
We use an **iterative depth-first search (recursive backtracker)**:

1. Start at the entry cell and mark it visited.
2. Repeatedly look at the current cell's unvisited neighbours. If there are
   any, pick one at random, knock down the wall between them, move there, and
   push it on a stack. If there are none, backtrack by popping the stack.
3. Continue until the stack is empty.

Because every cell is visited exactly once and a wall is removed only when
moving into an unvisited cell, the result is a **spanning tree of the grid**:
exactly one path between any two cells — a *perfect* maze.

### Why this algorithm
- It guarantees a perfect maze by construction (no isolated cells, no loops).
- It is simple to reason about and implement iteratively, so it has no
  recursion-depth limit on large mazes.
- It produces long, winding corridors with relatively few short dead-ends,
  which makes for visually pleasing and non-trivial mazes.

### Imperfect mazes (`PERFECT=False`)
After the perfect maze is built, extra interior walls are removed at random to
introduce loops, while avoiding fully-open 3×3 areas so the result still reads
as a maze rather than an open room.

### The "42" pattern
A fixed "42" logo of fully-closed, isolated cells is stamped into the centre
of the maze. These cells are blocked before generation so the maze routes
around them. If the maze is too small to fit the pattern, an error is raised.

## Output file format
The output file contains, in order:
- one line per maze row, with **one hexadecimal digit per cell** encoding its
  closed walls — bit 0 (`1`) = North, bit 1 (`2`) = East, bit 2 (`4`) = South,
  bit 3 (`8`) = West. A bit is set when the wall is closed (`F` = fully closed);
- a blank line;
- the entry cell as `x,y`;
- the exit cell as `x,y`;
- the shortest path from entry to exit as a string of `N`/`E`/`S`/`W` moves.

Every line ends with `\n`.

## Reusable module (`mazegen`)
`mazegen` is a self-contained module (standard library only) exposing the
`MazeGenerator` class. The structure it exposes is the in-memory grid of
`Cell` objects — this is **not** the same as the hex output-file format.

```python
from mazegen import MazeGenerator

# Instantiate with custom parameters (size, entry/exit, perfect, seed)
maze = MazeGenerator(
    width=20, height=15,
    entry=(0, 0), exit=(19, 14),
    perfect=True, seed=42,
)
maze.generate()

# Access the structure: grid[y][x], or get_cell(x, y) -> Cell
cell = maze.get_cell(0, 0)
print(cell.north, cell.east, cell.south, cell.west)  # wall booleans (True = closed)

# Access a solution: shortest path as N/E/S/W moves
path = maze.solve()
print("".join(path))

# Optionally write the hex-encoded output file
maze.write_output_file("maze.txt")
```

Passing `seed=<int>` makes generation reproducible; omitting it (or passing
`None`) produces a different maze each run.

## Features
- Terminal visualiser rendering walls, entry, exit, and the solution path
  using coloured blocks.
- Interactive loop:
  - regenerate a new maze,
  - show/hide the shortest path,
  - cycle the wall colours,
  - quit.
- Perfect and imperfect (looped) maze generation.
- Reproducible mazes via an optional seed.
- The "42" pattern.
- Reusable, pip-installable `mazegen` package.

## Resources
- Maze generation algorithm — Wikipedia:
  <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
- Jamis Buck, *Mazes for Programmers* / "The Buckblog" maze series — overview
  of the recursive backtracker and other algorithms.
- Thick / "wall-as-cell" maze rendering (the `(2n+1)` grid representation used
  by the visualiser).
- ANSI escape codes (terminal colours):
  <https://en.wikipedia.org/wiki/ANSI_escape_code>

### How AI was used
We used an AI assistant as a guide and reviewer rather than to
generate the project for us. Concretely, it helped with:
- explaining and debugging the visualiser's coordinate maths (the `(2n+1)`
  thick-maze rendering, entry/exit/path overlay);
- setting up the `flake8`/`mypy` configuration and diagnosing lint errors;
- planning the Git strategy for integrating the solver branch;
- diagnosing the "42" pattern bug and the 3×3-open-area constraint;
- explaining concepts (PRNG seeding, Python packaging) and drafting this README.

The core algorithms (BFS solver, "42" placement, generation) were implemented
and reviewed by the team; AI-suggested content was only kept where we
understood it and could defend it.

## Team and project management

### Roles
- **misousa (Miguel Sousa)** — maze generation core (`Cell`, `MazeGenerator`),
  BFS solver, perfect/imperfect generation, the "42" pattern, the hex output
  writer, and the `mazegen` package.
- **fgoncal2 (Francisco Abelha)** — configuration parser, application entry
  point, Makefile and tooling, the terminal visualiser (rendering + interaction
  loop), integration, and documentation.

### Planning and how it evolved
We started bottom-up: the cell/grid model and parser first, then generation and
the solver, then the visualiser, and finally packaging, the output writer, and
documentation. The main change from the initial plan was reorganising the
generator into a self-contained, importable package once the reusability
requirement became central.

### What worked well / what to improve
- *Worked well:* splitting the work along a clear module boundary, and keeping
  `make lint` green throughout.
- *To improve:* tighter coordination on shared files to avoid divergent
  branches, and writing tests earlier rather than at the end.

### Tools
Python 3.10+, `flake8`, `mypy`, `make`, `setuptools`/`build` for packaging,
Git/GitHub, and an AI assistant as described above.
