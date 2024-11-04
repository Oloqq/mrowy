from settings.simulation_settings import get_default_simulation_settings
from settings.display_settings import DisplaySettings
from simulation.simulation import PygameSimulation
from simulation.drawing import AntRenderer

def main():
    sim = PygameSimulation(
        "ant.npz",
        AntRenderer(),
        get_default_simulation_settings(),
        DisplaySettings()
        )
    sim.run()


if __name__ == "__main__":
    main()