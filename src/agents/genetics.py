import random
from src import config

def create_genome() -> dict:
    """
    Creates a new genome (a dictionary of traits).
    This is the 'replicator' data.
    """
    return {
        "aggression": random.uniform(0.0, 1.0), # NEW: Continuous aggression trait
        "speed": random.uniform(2.0, 4.0),
        "vision": random.uniform(8.0, 15.0),
        "mutation_multiplier": random.uniform(0.5, 1.5), # NEW: Meta-mutation gene
        "color": (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
    }

def crossover(parent1_genome: dict, parent2_genome: dict) -> dict:
    """
    Performs gene-by-gene crossover between two parents.
    For each gene, pick randomly from one of the two parents.
    """
    child_genome = {}
    for key in parent1_genome:
        child_genome[key] = random.choice([parent1_genome[key], parent2_genome[key]])
    return child_genome

def mutate(genome: dict) -> dict:
    """
    Applies mutations to a genome based on mutation rate and multiplier.
    This is a core part of the 'replicator' logic.
    """
    mutated_genome = genome.copy()
    
    # Get the vehicle's own mutation "meta-gene"
    multiplier = mutated_genome['mutation_multiplier']
    
    # Mutate Aggression (Gaussian shift)
    if random.random() < config.MUTATION_RATE:
        shift = random.uniform(-0.1, 0.1) * multiplier
        mutated_genome['aggression'] = clamp(mutated_genome['aggression'] + shift, 0.0, 1.0)

    # Mutate Speed
    if random.random() < config.MUTATION_RATE:
        shift = random.uniform(-0.2, 0.2) * multiplier
        mutated_genome['speed'] = max(1.0, mutated_genome['speed'] + shift)

    # Mutate Vision
    if random.random() < config.MUTATION_RATE:
        shift = random.uniform(-0.5, 0.5) * multiplier
        mutated_genome['vision'] = max(3.0, mutated_genome['vision'] + shift)

    # Mutate Color (complete re-roll)
    if random.random() < config.MUTATION_RATE:
        mutated_genome['color'] = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

    # Mutate the "meta-gene" itself!
    if random.random() < config.MUTATION_RATE_META: # Use a different rate
        shift = random.uniform(-0.1, 0.1)
        mutated_genome['mutation_multiplier'] = max(0.1, mutated_genome['mutation_multiplier'] + shift)
        
    return mutated_genome

def reproduce(parent1_genome: dict, parent2_genome: dict) -> dict:
    """
    Creates a new child genome by combining parent genomes,
    with crossover and then mutation.
    """
    # 1. Crossover
    child_genome = crossover(parent1_genome, parent2_genome)
    
    # 2. Mutation
    child_genome = mutate(child_genome)
    
    return child_genome

def clamp(value, min_val, max_val):
    """Helper function to keep a value within bounds."""
    return max(min_val, min(value, max_val))