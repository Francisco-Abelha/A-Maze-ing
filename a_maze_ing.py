from mazegen.mazegen import MazeGenerator
from parser import parser, Config
from visualiser import run
import sys


def main() -> None:
    """Run the A-Maze-ing application.

    The function reads the configuration file, creates the maze, places the
    42 pattern when possible, generates the maze, writes the output file, and
    starts the terminal visualiser.
    """
    try:
        config: Config = parser()
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
        run(maze, output_file)
    except (ValueError, KeyboardInterrupt) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
