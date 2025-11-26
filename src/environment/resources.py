from ursina import *
import random
from src import config

class Food(Entity):
    """
    A food resource in the world.
    """
    def __init__(self):
        super().__init__(
            model='sphere',
            color=color.green,
            scale=0.5,
            collider='sphere'
        )
        self.respawn()

    def respawn(self):
        """Moves the food to a new random location."""
        half_world = config.WORLD_SIZE / 2
        self.position = (
            random.uniform(-half_world, half_world),
            0.25, # Just above the ground
            random.uniform(-half_world, half_world)
        )