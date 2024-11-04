from simulation.node import Node

from pygame import Vector2
import numpy as np

class Ant:
    def __init__(self, position: Vector2):
        self.pos = position

    def step(self, grid: np.ndarray, objects: np.ndarray, nodes: list[list[Node]]):
        pass