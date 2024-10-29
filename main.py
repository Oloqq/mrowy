from simulation.simulation import PygameSimulation
from simulation.drawing import FoxRenderer

if __name__ == "__main__":
    sim = PygameSimulation(FoxRenderer())
    sim.run()
