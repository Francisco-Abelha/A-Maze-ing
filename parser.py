import sys
from typing import Callable, Any
from typing import TypedDict, NotRequired


class Config(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    PERFECT: bool
    OUTPUT_FILE: str
    SEED: NotRequired[int]


def validate_width(value: str) -> int:
    """Validate the maze width.

    Args:
        value: Width value read from the configuration file.

    Returns:
        The validated width as an integer.

    Raises:
        ValueError: If the width is not greater than zero.
    """
    if not value:
        raise ValueError("WIDTH cannot be empty")
    try:
        width: int = int(value)
    except ValueError:
        raise ValueError("WIDTH must be an integer")

    if width <= 0:
        raise ValueError("Width value must be greater than 0")

    return width


def validate_height(value: str) -> int:
    """Validate the maze height.

    Args:
        value: Height value read from the configuration file.

    Returns:
        The validated height as an integer.

    Raises:
        ValueError: If the height is not greater than zero.
    """
    if not value:
        raise ValueError("HEIGHT cannot be empty")
    try:
        height: int = int(value)
    except ValueError:
        raise ValueError("HEIGHT must be an integer")

    if height <= 0:
        raise ValueError("Height value must be greater than 0")

    return height


def validate_coordinates(value: str) -> tuple[int, int]:
    """Validate coordinates in the x,y format.

    Args:
        value: String containing coordinates in 'x,y' format.

    Returns:
        A tuple of two integers representing the coordinates.

    Raises:
        ValueError: If the format is invalid or cannot be converted.
    """
    if not value:
        raise ValueError("Coordinates cannot be empty")
    coordinates: list[str] = value.split(",")
    if len(coordinates) != 2:
        raise ValueError("Coordinates must be formated in x,y")
    try:
        x: int = int(coordinates[0])
        y: int = int(coordinates[1])
    except ValueError:
        raise ValueError("Coordinates must be integers")

    return (x, y)


def validate_perfect(value: str) -> bool:
    """Convert the PERFECT configuration value into a boolean.

    Args:
        value: String value of the PERFECT key from the configuration.

    Returns:
        Boolean representation of the value.

    Raises:
        ValueError: If the value is not 'True' or 'False'.
    """
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise ValueError("PERFECT must be either True or False")


def validate_output_file(value: str) -> str:
    """Validate the output filename.

    Args:
        value: Output filename from the configuration.

    Returns:
        The validated filename as a string.
    """
    if not value:
        raise ValueError("OUTPUT_FILE cannot be empty")
    return value


def validate_seed(value: str) -> int:
    """Validate and convert the seed into an integer.

    Args:
        value: Seed value from the configuration.

    Returns:
        The validated seed as an integer.

    Raises:
        ValueError: If the seed is not an integer.
    """
    if not value:
        raise ValueError("SEED cannot be empty")
    try:
        seed: int = int(value)
    except ValueError:
        raise ValueError("SEED must be an integer")
    return seed


def parser() -> Config:
    """Read and validate the configuration file.

    Returns:
        A dictionary containing the maze configuration.

    Raises:
        ValueError: If the configuration file is missing,
         invalid, or malformed.
    """
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
        "SEED": validate_seed,
    }

    config: dict[str, Any] = {}

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

    validated_config: Config = {
        "WIDTH": config["WIDTH"],
        "HEIGHT": config["HEIGHT"],
        "ENTRY": config["ENTRY"],
        "EXIT": config["EXIT"],
        "OUTPUT_FILE": config["OUTPUT_FILE"],
        "PERFECT": config["PERFECT"],
    }

    if "SEED" in config:
        validated_config["SEED"] = config["SEED"]

    return validated_config
