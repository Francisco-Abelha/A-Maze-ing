import sys
from typing import Callable, Any


def validate_width(value: str) -> int:
    width: int = int(value)

    if width <= 0:
        raise ValueError("Width value must be greater than 0")

    return width


def validate_height(value: str) -> int:
    height: int = int(value)

    if height <= 0:
        raise ValueError("Height value must be greater than 0")

    return height


def validate_coordinates(value: str) -> tuple[int, int]:
    coordinates: list[str] = value.split(",")
    if len(coordinates) != 2:
        raise ValueError("Coordinates must be formated in x,y")

    x: int = int(coordinates[0])
    y: int = int(coordinates[1])

    return (x, y)


def validate_perfect(value: str) -> bool:
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise ValueError("PERFECT must be either True or False")


def validate_output_file(value: str) -> str:
    if not value:
        raise ValueError("OUTPUT_FILE cannot be empty")
    return value


def validate_seed(value: str) -> int:
    try:
        seed: int = int(value)
    except ValueError:
        raise ValueError("SEED must be an integer")
    return seed


def parser() -> dict:
    args: int = len(sys.argv)

    if args != 2:
        raise ValueError("You need to pass one argument!")

    REQUIRED_KEYS: set[str] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    VALIDATORS: dict[str, Callable[[str], Any]] = {
        "WIDTH": validate_width,
        "HEIGHT": validate_height,
        "ENTRY": validate_coordinates,
        "EXIT": validate_coordinates,
        "OUTPUT_FILE": validate_output_file,
        "PERFECT": validate_perfect,
        "SEED": validate_seed
    }

    config: dict = {}

    try:
        with open(sys.argv[1], "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError("Invalid line format")

                key, value = line.split("=", 1)

                if key not in VALIDATORS:
                    raise ValueError(f"Unknown key: {key}")

                if key in config:
                    raise ValueError(f"Duplicate key: '{key}'")

                config[key] = VALIDATORS[key](value)
    except FileNotFoundError:
        raise ValueError(f"File '{sys.argv[1]}' not found")

    missing_keys = REQUIRED_KEYS - config.keys()

    if missing_keys:
        raise ValueError(f"Missing keys: {missing_keys}")

    return config
