from mazegen import MazeGenerator
from parser import parser
from visualiser import run
import sys


def main() -> None:
    try:
        config: dict = parser()
        width = config["WIDTH"]
        height = config["HEIGHT"]
        maze_entry = config["ENTRY"]
        maze_exit = config["EXIT"]
        perfect = config["PERFECT"]
        seed = config.get("SEED")
        output_file = config["OUTPUT_FILE"]

        maze = MazeGenerator(
            width, height, maze_entry, maze_exit, perfect, seed=seed
        )
        maze.add_42_pattern()
        maze.generate()
        maze.write_output_file(output_file)
        run(maze)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
