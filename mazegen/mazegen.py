import random
from dataclasses import dataclass
from collections import deque


@dataclass
class Cell:
    """Represent a single maze cell.

    Attributes:
        north: Whether the north wall is closed.
        south: Whether the south wall is closed.
        east: Whether the east wall is closed.
        west: Whether the west wall is closed.
        visited: Whether the cell was visited during generation.
        blocked: Whether the cell is reserved for the 42 pattern.
    """

    north: bool = True
    south: bool = True
    east: bool = True
    west: bool = True
    visited: bool = False
    blocked: bool = False


class MazeGenerator:
    """Generate, solve and export mazes.

    The generator creates a maze using recursive backtracking. It can keep the
    maze perfect or add extra openings to create loops. It also supports a
    centered 42 pattern made of blocked cells.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None = None,
    ) -> None:
        """Initialize a maze generator.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.
            entry: Entry cell coordinates as ``(x, y)``.
            exit: Exit cell coordinates as ``(x, y)``.
            perfect: Whether the maze should contain only one path between
                entry and exit.
            seed: Optional random seed for reproducible generation.

        Raises:
            ValueError: If the maze parameters are invalid.
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.rng = random.Random(seed)
        self.perfect = perfect
        self.validate_parameters()

        self.grid = []
        for _ in range(height):
            row = []

            for _ in range(width):
                row.append(Cell())

            self.grid.append(row)

    def validate_parameters(self) -> None:
        """Validate maze dimensions and entry/exit coordinates.

        Raises:
            ValueError: If dimensions are invalid, coordinates are outside the
                maze bounds, or entry and exit are equal.
        """
        if self.width <= 0:
            raise ValueError("WIDTH must be greater than 0")
        if self.height <= 0:
            raise ValueError("HEIGHT must be greater than 0")

        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit

        if not (0 <= entry_x < self.width and 0 <= entry_y < self.height):
            raise ValueError("ENTRY must be inside the maze bounds")
        if not (0 <= exit_x < self.width and 0 <= exit_y < self.height):
            raise ValueError("EXIT must be inside the maze bounds")

        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different")

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the cell at the given coordinates.

        Args:
            x: Horizontal cell coordinate.
            y: Vertical cell coordinate.

        Returns:
            The cell stored at ``(x, y)``.
        """
        return self.grid[y][x]

    def remove_wall(
        self, current_x: int, current_y: int, next_x: int, next_y: int
    ) -> None:
        """Remove the wall between two adjacent cells.

        Args:
            current_x: X coordinate of the current cell.
            current_y: Y coordinate of the current cell.
            next_x: X coordinate of the neighbouring cell.
            next_y: Y coordinate of the neighbouring cell.
        """
        if next_x > current_x:
            self.get_cell(current_x, current_y).east = False
            self.get_cell(next_x, next_y).west = False
        if next_x < current_x:
            self.get_cell(current_x, current_y).west = False
            self.get_cell(next_x, next_y).east = False
        if next_y < current_y:
            self.get_cell(current_x, current_y).north = False
            self.get_cell(next_x, next_y).south = False
        if next_y > current_y:
            self.get_cell(current_x, current_y).south = False
            self.get_cell(next_x, next_y).north = False

    def get_unvisited_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return valid neighbouring cells that were not visited yet.

        Args:
            x: Horizontal cell coordinate.
            y: Vertical cell coordinate.

        Returns:
            A list of unvisited and non-blocked neighbour coordinates.
        """
        neighbors = []

        directions = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

        for nx, ny in directions:
            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and not self.get_cell(nx, ny).visited
                and not self.get_cell(nx, ny).blocked
            ):
                neighbors.append((nx, ny))

        return neighbors

    def generate(self) -> None:
        """Generate the maze using recursive backtracking.

        The method starts from the entry cell, visits every reachable
        non-blocked cell, and removes walls to create passages. If ``perfect``
        is false, it adds extra openings after the perfect maze is generated.
        """
        start_x: int = self.entry[0]
        start_y: int = self.entry[1]

        stack: list[tuple[int, int]] = [(start_x, start_y)]
        self.get_cell(start_x, start_y).visited = True

        while stack:
            current_x, current_y = stack[-1]
            neighbors = self.get_unvisited_neighbors(current_x, current_y)

            if neighbors:
                next_x, next_y = self.rng.choice(neighbors)
                self.remove_wall(current_x, current_y, next_x, next_y)
                self.get_cell(next_x, next_y).visited = True
                stack.append((next_x, next_y))

            else:
                stack.pop()

        if not self.perfect:
            self.add_extra_openings()

    def get_accessible_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[tuple[int, int]]:
        """Return neighbours that can be reached through open walls.

        Args:
            x: Horizontal cell coordinate.
            y: Vertical cell coordinate.

        Returns:
            A list of accessible neighbour coordinates.
        """
        neighbors = []
        cell = self.get_cell(x, y)

        if not cell.north:
            neighbors.append((x, y - 1))

        if not cell.south:
            neighbors.append((x, y + 1))

        if not cell.east:
            neighbors.append((x + 1, y))

        if not cell.west:
            neighbors.append((x - 1, y))

        return neighbors

    def solve(self) -> list[str]:
        """Find the shortest path from entry to exit.

        Uses breadth-first search to find the shortest valid path through open
        passages.

        Returns:
            A list of directions using ``N``, ``E``, ``S`` and ``W``.

        Raises:
            ValueError: If no path exists between entry and exit.
        """
        queue = deque([self.entry])

        visited = {self.entry}
        parents: dict = {self.entry: None}

        while queue:
            current = queue.popleft()
            if current == self.exit:
                break

            neighbors = self.get_accessible_neighbors(current[0], current[1])

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parents[neighbor] = current
                    queue.append(neighbor)

        path = []
        current = self.exit

        if self.exit not in parents:
            raise ValueError("No path found between entry and exit")

        while current is not None:
            path.append(current)
            current = parents[current]

        path.reverse()
        new_path: list[str] = []

        x = 1
        while x < len(path):
            cell = path[x - 1]
            next_cell = path[x]
            if cell[0] < next_cell[0]:
                new_path.append("E")
            if cell[0] > next_cell[0]:
                new_path.append("W")
            if cell[1] < next_cell[1]:
                new_path.append("S")
            if cell[1] > next_cell[1]:
                new_path.append("N")
            x += 1

        return new_path

    def print_visited(self) -> None:
        """Print a debug view of visited cells."""
        for row in self.grid:
            for cell in row:
                print("-" if cell.visited else "*", end=" ")
            print()

    def close_cell(self, x: int, y: int) -> None:
        """Close all walls of a cell and update neighbouring walls.

        Args:
            x: Horizontal cell coordinate.
            y: Vertical cell coordinate.
        """
        cell = self.get_cell(x, y)

        cell.north = True
        cell.south = True
        cell.east = True
        cell.west = True

        if x > 0:
            self.get_cell(x - 1, y).east = True
        if x < self.width - 1:
            self.get_cell(x + 1, y).west = True
        if y > 0:
            self.get_cell(x, y - 1).south = True
        if y < self.height - 1:
            self.get_cell(x, y + 1).north = True

    def add_42_pattern(self) -> None:
        """Place a centered 42 pattern using blocked cells.

        The pattern is omitted when the maze is too small.
        Entry and exit cannot overlap the blocked cells.

        Raises:
            ValueError: If entry or exit overlaps the 42 pattern.
        """
        pattern_width = 7
        pattern_height = 5

        if self.width < pattern_width or self.height < pattern_height:
            print("Maze too small to draw 42 pattern\n")
            return

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        four = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
        ]

        two = [
            (4, 0),
            (5, 0),
            (6, 0),
            (6, 1),
            (6, 2),
            (5, 2),
            (4, 2),
            (4, 3),
            (4, 4),
            (5, 4),
            (6, 4),
        ]

        pattern_cells = [(start_x + dx, start_y + dy) for dx, dy in four + two]

        if self.entry in pattern_cells:
            raise ValueError("ENTRY overlaps the 42 pattern")
        if self.exit in pattern_cells:
            raise ValueError("EXIT overlaps the 42 pattern")

        for x, y in pattern_cells:
            self.get_cell(x, y).blocked = True
            self.close_cell(x, y)

    def add_extra_openings(self) -> None:
        """Open random extra walls to create a non-perfect maze.

        Blocked cells are ignored so the 42 pattern remains fully closed.
        """

        for y in range(self.height):
            for x in range(self.width):
                current = self.get_cell(x, y)
                if current.blocked:
                    continue

                possible_neighbors = []

                if x + 1 < self.width:
                    possible_neighbors.append((x + 1, y))
                if y + 1 < self.height:
                    possible_neighbors.append((x, y + 1))

                for nx, ny in possible_neighbors:
                    neighbor = self.get_cell(nx, ny)
                    if neighbor.blocked:
                        continue
                    if self.rng.random() < 0.15:
                        self.remove_wall(x, y, nx, ny)

    def cell_to_hex(self, cell: Cell) -> str:
        """Convert a cell's walls into one hexadecimal digit.

        Args:
            cell: Cell to convert.

        Returns:
            A hexadecimal character representing closed walls.
        """
        value = 0

        if cell.north:
            value += 1
        if cell.east:
            value += 2
        if cell.south:
            value += 4
        if cell.west:
            value += 8

        return format(value, "X")

    def get_hex_lines(self) -> list[str]:
        """Return the maze encoded as hexadecimal text lines.

        Returns:
            A list where each string represents one row of the maze.
        """
        lines = []

        for row in self.grid:
            line = ""
            for cell in row:
                line += self.cell_to_hex(cell)
            lines.append(line)

        return lines

    def write_output_file(self, output_file: str) -> None:
        """Write the maze, entry, exit and solution path to a file.

        Args:
            output_file: Destination file path.
        """
        path = "".join(self.solve())

        with open(output_file, "w") as file:
            for line in self.get_hex_lines():
                file.write(line + "\n")

            file.write("\n")
            file.write(f"{self.entry[0]},{self.entry[1]}\n")
            file.write(f"{self.exit[0]},{self.exit[1]}\n")
            file.write(path + "\n")
