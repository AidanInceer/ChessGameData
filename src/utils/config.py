from dataclasses import dataclass


@dataclass
class Config:
    username: str
    games: int
    depth: int
