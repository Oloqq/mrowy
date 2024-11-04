import numpy as np

PerColony = list
Intensity = float

class Node:
    def __init__(self, neighborhood: tuple[bool, bool, bool, bool]):
        # neighbor order: top, right, bottom, left
        self.has_neighbor: np.ndarray = np.array(neighborhood)
        TMP_NUM_COLONIES = 1 # set it in simulation_settings
        self.pheromones: PerColony[(Intensity, Intensity, Intensity, Intensity)] = [
            np.zeros(4) for _ in range(TMP_NUM_COLONIES)
        ]
        TMP_CAPACITY = 6 # how to determine?
        self.capacity = TMP_CAPACITY
        self.spare_capacity = self.capacity

