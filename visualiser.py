import mazegen


def visualiser(maze: mazegen.MazeGenerator):
    w = 2 * maze.width + 1
    h = 2 * maze.height + 1
    color_white = "\033[47m  \033[0m"
    color_black = "\033[40m  \033[0m"
    color_pink = "\033[48;2;255;105;180m  \033[0m"
    color_green = "\033[42m  \033[0m"
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
