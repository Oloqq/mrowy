from settings.simulation_settings import get_default_simulation_settings
from settings.display_settings import DisplaySettings
from simulation.simulation import PygameSimulation
from simulation.drawing import FoxRenderer

def start_gridnpz():
    sim = PygameSimulation(
        "grid.npz",
        FoxRenderer(),
        get_default_simulation_settings(),
        DisplaySettings()
        )
    sim.run()

def start_fresh():
    sim = PygameSimulation(
        "asdas",
        FoxRenderer(),
        get_default_simulation_settings(),
        DisplaySettings()
        )
    sim.run()

if __name__ == "__main__":
    start_gridnpz()
    # start_fresh()