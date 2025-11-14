import matplotlib.pyplot as plt
from src.organism import Organism
from src.genetics import random_genome, evaluate_fitness
from src.evolution import selection, reproduce

# --- PARAMETERS ---
POP_SIZE = 100
GENOME_LENGTH = 20
MUTATION_RATE = 0.01
GENERATIONS = 100
TARGET = "11001100110011001100"

# --- INITIALIZATION ---
population = [Organism(random_genome(GENOME_LENGTH)) for _ in range(POP_SIZE)]
best_fitness_history = []

# --- EVOLUTION LOOP ---
for generation in range(GENERATIONS):
    for org in population:
        org.fitness = evaluate_fitness(org.genome, TARGET)

    best = max(population, key=lambda o: o.fitness)
    best_fitness_history.append(best.fitness)

    print(f"Gen {generation:03d}: Best genome = {best.genome} | Fitness = {best.fitness}")

    parents = selection(population)
    population = list(reproduce(parents, MUTATION_RATE))

# --- VISUALIZATION ---
plt.plot(best_fitness_history)
plt.title("Evolution of Fitness Over Generations")
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.show()
