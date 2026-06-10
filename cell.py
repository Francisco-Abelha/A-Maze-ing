from dataclasses import dataclass


@dataclass
class Cell:
    north: bool = True
    south: bool = True
    east: bool = True
    west: bool = True
    visited: bool = False
