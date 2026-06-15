from mazegen import MazeGenerator


def build_path_set(maze: MazeGenerator) -> set[tuple[int, int]]:
    fill = (2 * maze.entry[0] + 1, 2 * maze.entry[1] + 1)
    path_set = {fill}
    deltas = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    for letter in maze.solve():
        dx, dy = deltas[letter]
        for _ in range(2):
            fill = (fill[0] + dx, fill[1] + dy)
            path_set.add(fill)    
    return path_set


def render(maze: MazeGenerator, show_path: bool, path_set: set) -> None:
    w = 2 * maze.width + 1
    h = 2 * maze.height + 1
    color_white = "\033[47m  \033[0m"
    color_black = "\033[40m  \033[0m"
    color_pink = "\033[48;2;255;105;180m  \033[0m"
    color_green = "\033[42m  \033[0m"
    color_blue = "\033[44m  \033[0m"
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
                block = color_white
            elif x % 2 == 1 and y % 2 == 1:
                block = color_black
            elif x == 0 or x == w - 1 or y == 0 or y == h - 1:
                block = color_white
            elif x % 2 == 1:
                wall = maze.get_cell((x - 1) // 2, y // 2).north
                block = color_white if wall else color_black
            else:
                wall = maze.get_cell(x // 2, (y - 1) // 2).west
                block = color_white if wall else color_black
            row += block
        print(row)


def run(maze: MazeGenerator) -> None:
    show_path = False
    path_set = build_path_set(maze)
    while True:
        print("\033[2J\033[H", end="")
        render(maze, show_path, path_set)
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
            maze.generate()
            path_set = build_path_set(maze)
        elif choice == "2":
            show_path = not show_path
        elif choice == "4":
            break
