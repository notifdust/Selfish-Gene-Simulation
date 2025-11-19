# The Selfish Gene: Digital Evolution Model

## Project Overview

This Python project is a simple simulation of **Digital Evolution** inspired by the concepts presented in Richard Dawkins' book, ***The Selfish Gene***.

The core aim is to model how a population of digital organisms, represented by simple binary genomes, evolves over generations toward a predefined **target genome** through the mechanisms of natural selection, reproduction, mutation, and crossover.

It demonstrates that even simple, self-replicating entities can, over time, exhibit complex adaptation when subjected to differential survival pressure (fitness).

## How It Works

The simulation follows a standard **Genetic Algorithm** loop:

1.  **Initialization:** A random starting population of organisms is created.
2.  **Evaluation:** Each organism's **fitness** is calculated based on how closely its genome matches the fixed target genome (a measure of Hamming similarity).
3.  **Selection:** Parents are chosen from the population, with a bias towards those having higher fitness.
4.  **Reproduction:** The selected parents generate the next generation through **crossover** and **mutation**.
5.  **Iteration:** The new generation replaces the old one, and the process repeats for a set number of generations.

The progress is tracked and visualized by plotting the best fitness achieved in each generation.

## Structure

The project is organized into a `src/` directory containing the core evolutionary components:

. ├── main.py # Entry point, sets parameters, runs the evolution loop, and handles visualization. └── src/ ├── organism.py # Defines the Organism class (holds genome and fitness). ├── genetics.py # Handles random genome creation and fitness calculation. └── evolution.py # Implements selection, crossover, and mutation mechanisms.


## Key Parameters

The main configuration parameters are defined at the top of `main.py`:

| Parameter | Value (Default) | Description |
| :--- | :--- | :--- |
| `POP_SIZE` | `100` | The number of organisms in the population. |
| `GENOME_LENGTH` | `20` | The length of the binary genome (e.g., "11001..."). |
| `MUTATION_RATE` | `0.01` | The probability that any single bit (gene) will flip during reproduction. |
| `GENERATIONS` | `100` | The total number of cycles the simulation will run. |
| `TARGET` | `"11001100110011001100"` | The ideal, unachievable target genome the population evolves toward. |

## Requirements

You will need Python 3 and `matplotlib` for the visualization.

```bash
pip install matplotlib
▶️ Running the Simulation
Execute the main.py file from the project root directory:

Bash

python main.py
The console output will show the best genome and its fitness for each generation. Once complete, a graph will appear showing the fitness progression over time.
``` 
## Next Steps & Extensions
Future extensions could involve exploring different evolutionary concepts:

Different Selection Methods: Implement Roulette Wheel or Rank-Based selection (currently uses Tournament Selection).

Elitism: Preserve the highest-fitness individual across generations to prevent loss of beneficial traits.

Varying Genetic Operators: Implement Two-Point Crossover for greater genetic mixing.

Environmental Change: Implement a dynamic target genome (changing environment) to observe adaptation pressure.
