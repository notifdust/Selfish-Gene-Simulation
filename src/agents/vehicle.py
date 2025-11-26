from ursina import *
import random
from src import config
from src import simulation # Import global lists
from src.agents import genetics
from src.agents import behavior

class Vehicle(Entity):
    """
    Represents the 'vehicle' or 'survival machine'.
    This class manages the agent's data, state, and action *resolution*.
    The 'brain' (seeking/wandering) is in the behavior.py module.
    """
    def __init__(self, genome: dict, position: tuple):
        super().__init__(
            model='cone',
            scale=(0.6, 1.0, 0.6),
            position=position,
            collider='box'
        )
        self.genome = genome
        self.energy = config.STARTING_ENERGY
        self.state = "WANDERING"
        self.target = None 
        
        # Apply genetic traits
        self.apply_genetics()

    def apply_genetics(self):
        self.speed = self.genome['speed']
        self.vision = self.genome['vision']
        self.update_color()
        
    def update_color(self):
        """Color is now a gradient based on aggression."""
        # Red = Aggressive (Hawk), Blue = Passive (Dove)
        r = self.genome['aggression']
        b = 1.0 - self.genome['aggression']
        self.color = color.color(0, r, b) # (h, s, v) -> (0, R, B) is not right
        self.color = color.rgb(r * 255, 0, b * 255) # Use RGB

    def eat(self, food_item):
        """Called when this vehicle reaches a food item."""
        competitor = None
        for other in simulation.population:
            if other != self and other.state == "SEEKING_FOOD" and distance(other, food_item) < 1.0:
                competitor = other
                break
        
        if competitor:
            self.compete(competitor, food_item)
        else:
            self.energy += config.ENERGY_GAIN_FOOD
            food_item.respawn()
        
        self.target = None

    def compete(self, other, resource):
        """
        Executes the Hawk-Dove game logic using the continuous aggression gene.
        """
        
        # Determine strategy from aggression gene
        my_strategy = "HAWK" if self.genome['aggression'] > config.AGGRESSION_THRESHOLD else "DOVE"
        other_strategy = "HAWK" if other.genome['aggression'] > config.AGGRESSION_THRESHOLD else "DOVE"
        
        V = config.RESOURCE_VALUE
        C = config.FIGHT_COST
        D = config.DISPLAY_COST

        winner = None
        
        if my_strategy == "HAWK" and other_strategy == "HAWK":
            self.energy -= C / 2
            other.energy -= C / 2
            winner = random.choice([self, other])
        elif my_strategy == "HAWK" and other_strategy == "DOVE":
            winner = self
            other.energy -= D
        elif my_strategy == "DOVE" and other_strategy == "HAWK":
            winner = other
            self.energy -= D
        elif my_strategy == "DOVE" and other_strategy == "DOVE":
            self.energy -= D
            other.energy -= D
            winner = random.choice([self, other])

        if winner == self:
            self.energy += V
        elif winner == other:
            other.energy += V
            
        resource.respawn()
        self.target = None
        other.target = None

    def mate(self, partner):
        """Reproduces with a partner."""
        if not self.enabled or not partner.enabled:
            return
            
        child_genome = genetics.reproduce(self.genome, partner.genome)
        
        self.energy -= config.ENERGY_COST_REPRODUCE
        partner.energy -= config.ENERGY_COST_REPRODUCE
        
        new_pos = self.position + (random.uniform(-1,1), 0, random.uniform(-1,1))
        child = Vehicle(genome=child_genome, position=new_pos)
        simulation.population.append(child)
        
        self.state = "WANDERING"
        partner.state = "WANDERING"
        self.target = None
        partner.target = None

    def die(self):
        """Vehicle dies from lack of energy."""
        if self in simulation.population:
            simulation.population.remove(self)
        self.enabled = False
        destroy(self)

    def update(self):
        """
        Main loop for each vehicle, called once per frame by main.py.
        Delegates logic to the behavior module.
        """
        self.energy -= config.ENERGY_COST_MOVE * self.speed * time.dt
        
        # 1. Update state (brain)
        behavior.update_state(self)
        
        # 2. Perform action (brain/body)
        behavior.perform_action(self)