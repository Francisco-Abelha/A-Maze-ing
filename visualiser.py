from mazegen.mazegen import MazeGenerator

WALL_COLORS = [
    "\033[47m  \033[0m",  # white
    "\033[43m  \033[0m",  # yellow
    "\033[46m  \033[0m",  # cyan
    "\033[45m  \033[0m",  # magenta
]


def build_path_set(maze: MazeGenerator) -> set[tuple[int, int]]:
    """Build the set of coordinates used to display the solution path.

    Args:
        maze: An instance of MazeGenerator.

    Returns:
        A set of (x, y) tuples representing the solution path in the maze.
    """
    fill = (2 * maze.entry[0] + 1, 2 * maze.entry[1] + 1)
    path_set = {fill}
    deltas = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    for letter in maze.solve():
        dx, dy = deltas[letter]
        for _ in range(2):
            fill = (fill[0] + dx, fill[1] + dy)
            path_set.add(fill)
    return path_set


def render(
    maze: MazeGenerator, show_path: bool, path_set: set, wall_color: str
) -> None:
    """Render the maze in the terminal using ANSI colors.

    Args:
        maze (MazeGenerator): The maze to render.
        show_path (bool): Whether to display the solution path.
        path_set (set): The set of coordinates that form the solution path.
        wall_color (str): The ANSI color code to use for the maze walls.
    """
    w = 2 * maze.width + 1
    h = 2 * maze.height + 1
    color_black = "\033[40m  \033[0m"
    color_pink = "\033[48;2;255;105;180m  \033[0m"
    color_green = "\033[42m  \033[0m"
    color_blue = "\033[44m  \033[0m"
    color_gray = "\033[100m  \033[0m"
    entry_rx = 2 * maze.entry[0] + 1
    entry_ry = 2 * maze.entry[1] + 1
    exit_rx = 2 * maze.exit[0] + 1
    exit_ry = 2 * maze.exit[1] + 1
    for y in range(h):
        row = ""
        for x in range(w):
            if x == entry_rx and y == entry_ry:
                block = color_pink
            elif x == exit_rx and y == exit_ry:
                block = color_green
            elif show_path and (x, y) in path_set:
                block = color_blue
            elif x % 2 == 0 and y % 2 == 0:
                block = wall_color
            elif x % 2 == 1 and y % 2 == 1:
                cell = maze.get_cell((x - 1) // 2, (y - 1) // 2)
                block = color_gray if cell.blocked else color_black
            elif x == 0 or x == w - 1 or y == 0 or y == h - 1:
                block = wall_color
            elif x % 2 == 1:
                wall = maze.get_cell((x - 1) // 2, y // 2).north
                block = wall_color if wall else color_black
            else:
                wall = maze.get_cell(x // 2, (y - 1) // 2).west
                block = wall_color if wall else color_black
            row += block
        print(row)


def run(maze: MazeGenerator, output_file: str) -> None:
    """Run the interactive terminal visualiser.

    The visualiser lets the user regenerate the maze, show or hide the
    shortest path, rotate wall colours, and quit the program.

    Args:
        maze: Maze instance to display and interact with.
    """
    show_path = False
    color_index = 0
    path_set = build_path_set(maze)
    while True:
        print("\033[2J\033[H", end="")
        render(maze, show_path, path_set, WALL_COLORS[color_index])
        print("=== A-Maze-ing ===")
        print(
            "1: Re-generate a new maze\n"
            "2: Show/Hide path from entry to exit\n"
            "3: Rotate maze colors\n"
            "4: Quit\n"
        )
        choice = input("Choice? (1-4): ").strip()
        if choice == "1":
            maze = MazeGenerator(
                maze.width, maze.height, maze.entry, maze.exit, maze.perfect
            )
            maze.add_42_pattern()
            maze.generate()
            maze.write_output_file(output_file)
            path_set = build_path_set(maze)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(WALL_COLORS)
        elif choice == "4":
            break
