from mazegen import MazeGenerator
from parser import parser
from visualiser import visualiser
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

        maze = MazeGenerator(
            width, height, maze_entry, maze_exit, perfect, seed=seed
        )

        maze.generate()
        maze.dump()
        #print("->".join(maze.solve()))
        visualiser(maze)
        #print("->".join(maze.solve()))
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
