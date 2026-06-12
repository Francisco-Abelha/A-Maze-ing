from mazegen import MazeGenerator
from parser import parser
import sys


def main() -> None:
    try:
        config: dict = parser()
        width = config["WIDTH"]
        height = config["HEIGHT"]
        maze_entry = config["ENTRY"]
        maze_exit = config["EXIT"]
        perfect = config["PERFECT"]

        maze = MazeGenerator(width, height, maze_entry, maze_exit, perfect)
        maze.generate()
        maze.dump()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()