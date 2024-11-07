from settings.simulation_settings import get_default_simulation_settings
from settings.display_settings import DisplaySettings
from simulation.simulation import PygameSimulation
from simulation.drawing import AntRenderer

def main(sim_settings):
    sim = PygameSimulation(
        "ant.npz",
        AntRenderer(),
        sim_settings,
        DisplaySettings()
        )
    sim.run()


if __name__ == "__main__":
    sim_settings = get_default_simulation_settings()
    sim_settings.generic.create_grid_from_img = False
    main(sim_settings)
