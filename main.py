from ursina import *
import random
from src import config
from src import simulation # Import the global lists
from src.environment.world import Ground
from src.environment.resources import Food
from src.agents.vehicle import Vehicle
from src.agents.genetics import create_genome

def main():
    app = Ursina()

    # --- Setup World ---
    Ground()
    EditorCamera()
    camera.position = (0, 60, -60)
    camera.rotation_x = 45

    # --- Initialize Population and Food ---
    # Populate the global lists in the 'simulation' module
    simulation.food_items = [Food() for _ in range(config.STARTING_FOOD)]

    for _ in range(config.STARTING_POPULATION):
        pos = (
            random.uniform(-config.WORLD_SIZE/2, config.WORLD_SIZE/2),
            0.5,
            random.uniform(-config.WORLD_SIZE/2, config.WORLD_SIZE/2)
        )
        genome = create_genome()
        v = Vehicle(genome=genome, position=pos)
        simulation.population.append(v)

    # --- UI for Stats ---
    stats_text = Text(
        origin=(-0.5, -0.5), 
        position=window.top_left + (0.01, -0.01),
        scale=(1, 1)
    )

    def update():
        """
        This is the main simulation loop, called by Ursina every frame.
        """
        # We iterate over a copy [:] because the list can change
        for v in simulation.population[:]:
            if v.enabled:
                v.update() # Call each vehicle's update method

        # Update stats UI
        pop_count = len(simulation.population)
        if pop_count == 0:
            stats_text.text = "POPULATION EXTINCT"
            return
            
        avg_aggression = sum(v.genome['aggression'] for v in simulation.population) / pop_count
        avg_speed = sum(v.genome['speed'] for v in simulation.population) / pop_count
        avg_vision = sum(v.genome['vision'] for v in simulation.population) / pop_count
        avg_meta_mut = sum(v.genome['mutation_multiplier'] for v in simulation.m.population) / pop_count

        stats_text.text = f"Population: {pop_count}\n" \
                          f"Avg. Aggression: {avg_aggression:.2f} (Red=High, Blue=Low)\n" \
                          f"Avg. Speed: {avg_speed:.2f}\n" \
                          f"Avg. Vision: {avg_vision:.2f}\n" \
                          f"Avg. Mut-Multiplier: {avg_meta_mut:.2f}"

    app.run()

if __name__ == "__main__":
    main()