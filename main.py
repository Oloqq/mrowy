from settings.simulation_settings import get_default_simulation_settings
from settings.display_settings import DisplaySettings
from simulation.simulation import PygameSimulation
from simulation.drawing import AntRenderer

if __name__ == "__main__":
    sim_settings = get_default_simulation_settings()
    sim_settings.generic.simple_map = False
    sim_settings.generic.create_grid_from_img = True and not sim_settings.generic.simple_map
    save_name = "ant.npz" if sim_settings.generic.simple_map else "agh.npz"

    sim = PygameSimulation(
        save_name,
        AntRenderer(),
        sim_settings,
        DisplaySettings()
        )
    sim.run()
