from cell import Cell
import random


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
                next_x, next_y = random.choice(neighbors)
                self.remove_wall(current_x, current_y, next_x, next_y)
                self.get_cell(next_x, next_y).visited = True
                stack.append((next_x, next_y))

            else:
                stack.pop()

    def print_visited(self) -> None:
        for row in self.grid:
            for cell in row:
                print("1" if cell.visited else "0", end=" ")
            print()

    def print_walls(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                print(
                    f"({x},{y}) "
                    f"N:{cell.north} "
                    f"E:{cell.east} "
                    f"S:{cell.south} "
                    f"W:{cell.west}"
                )

    # def solve(self) -> list[str]:
    #     pass


if __name__ == "__main__":
    maze = MazeGenerator(
        width=15, height=20, entry=(0, 0), exit=(14, 19), perfect=True
    )
    maze.generate()
    visited_count = 0

    maze.print_visited()
    maze.print_walls()
