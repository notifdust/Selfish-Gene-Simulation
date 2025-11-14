import numpy as np
from .organism import Organism
from .genetics import crossover, mutate

def selection(population):
    total_fitness = sum(o.fitness for o in population)
    if total_fitness == 0:
        return np.random.choice(population, size=len(population))
    probabilities = [o.fitness / total_fitness for o in population]
    return np.random.choice(population, size=len(population), p=probabilities)

def reproduce(parents, mutation_rate):
    offspring = []
    for _ in range(len(parents)//2):
        p1, p2 = np.random.choice(parents, 2, replace=False)
        child_genome = mutate(crossover(p1.genome, p2.genome), mutation_rate)
        offspring.append(Organism(child_genome))
    return offspring
