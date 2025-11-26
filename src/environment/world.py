from ursina import *
from src import config

class Ground(Entity):
    """
    A simple ground plane for the simulation.
    """
    def __init__(self):
        super().__init__(
            model='plane',
            scale=(config.WORLD_SIZE, 1, config.WORLD_SIZE),
            color=color.rgb(100, 100, 100),
            texture='white_cube',
            texture_scale=(config.WORLD_SIZE, config.WORLD_SIZE),
            collider='box'
        )