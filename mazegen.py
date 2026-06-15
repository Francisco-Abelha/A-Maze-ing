import random
from dataclasses import dataclass
from collections import deque


@dataclass
class Cell:
    north: bool = True
    south: bool = True
    east: bool = True
    west: bool = True
    visited: bool = False
    blocked: bool = False


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.rng = random.Random(seed)
        self.perfect = perfect

        self.grid = []
        for _ in range(height):
            row = []

            for _ in range(width):
                row.append(Cell())

            self.grid.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def remove_wall(self, current_x, current_y, next_x, next_y) -> None:
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
        if self.exit not in parents:
            raise ValueError("No path found between entry and exit")
        current = self.exit

        while current is not None:
            path.append(current)
            current = parents[current]

        path.reverse()
        new_path: list[str] = []

        x = 1
        while x < len(path):
            cell = path[x - 1]
            next = path[x]
            if cell[0] < next[0]:
                new_path.append("E")
            if cell[0] > next[0]:
                new_path.append("W")
            if cell[1] < next[1]:
                new_path.append("S")
            if cell[1] > next[1]:
                new_path.append("N")
            x += 1

        return new_path

    def print_visited(self) -> None:
        for row in self.grid:
            for cell in row:
                print("-" if cell.visited else "*", end=" ")
            print()

    def dump(self):
        print("+" + "---+" * self.width)
        for y in range(self.height):
            line = "|"
            for x in range(self.width):
                line += "   " + ("|" if self.get_cell(x, y).east else " ")
            print(line)
            floor = "+"
            for x in range(self.width):
                floor += ("---" if self.get_cell(x, y).south else "   ") + "+"
            print(floor)

    def close_cell(self, x: int, y: int) -> None:
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
        pattern_width = 7
        pattern_height = 5

        if self.width < pattern_width or self.height < pattern_height:
            raise ValueError("Maze too small to draw 42 pattern")

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        four = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
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

        if self.entry in pattern_cells or self.exit in pattern_cells:
            print("42 pattern overlaps entry or exit")
            return

        for x, y in pattern_cells:
            self.get_cell(x, y).blocked = True
            self.close_cell(x, y)

    def add_extra_openings(self) -> None:

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


if __name__ == "__main__":
    maze = MazeGenerator(
        width=15, height=20, entry=(0, 0), exit=(14, 19), perfect=True
    )
    maze.generate()
    visited_count = 0

    maze.dump()
