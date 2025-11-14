import numpy as np

def random_genome(length):
    return ''.join(np.random.choice(['0', '1']) for _ in range(length))

def evaluate_fitness(genome, target):
    return sum(g == t for g, t in zip(genome, target))

def crossover(genome1, genome2):
    point = np.random.randint(1, len(genome1) - 1)
    return genome1[:point] + genome2[point:]

def mutate(genome, rate=0.01):
    return ''.join(
        bit if np.random.rand() > rate else ('1' if bit == '0' else '0')
        for bit in genome
    )
