# The Selfish Gene: An Agent-Based 3D Simulation

## Project Overview

This project is an advanced **Agent-Based Simulation** built in Python with the `ursina` 3D engine. It is inspired by the core concepts of evolutionary biology as described in Richard Dawkins' *The Selfish Gene*.

Unlike a simple genetic algorithm, this simulation models a "bottom-up" ecosystem. Digital organisms, or **"Vehicles,"** live, move, compete, and reproduce in a 3D world in real-time. Selection is not a discrete step but an **emergent property**: vehicles with "bad" genes (e.g., too slow, poor strategy, low vision) will fail to get enough energy to reproduce and will be removed from the gene pool upon "death."

## Core Concepts Modeled

* **Vehicle vs. Replicator:** The simulation explicitly separates the **Vehicle** (the `src/agents/vehicle.py` class, the "body") from the **Replicator** (the `src/agents/genetics.py` module, the "genes"). The `Vehicle` is the survival machine whose success is determined by its behavior; the `genome` is the data that gets replicated and passed on.
* **Evolutionarily Stable Strategy (ESS):** The simulation models the classic **Hawk-Dove** game.
    * This is not a binary "Hawk" or "Dove" gene. Instead, there is a continuous `aggression` gene (a float from 0.0 to 1.0).
    * Any vehicle with `aggression` above a threshold (e.g., 0.5) will *act* as a **Hawk** in a conflict.
    * Any vehicle below the threshold will *act* as a **Dove**.
    * By tracking the population's average aggression, we can see if it settles at a stable "ESS" value.
* **Evolution of Evolvability (Meta-Mutation):** A "meta-gene" called `mutation_multiplier` exists in the genome. This gene controls the *magnitude* of other mutations. Because this gene *itself* mutates, the population can evolve to be more (or less) mutable in response to selection pressure.

---

## Project Structure

The project is divided into a modular structure for clarity and scalability:

```
.
├── main.py                 # Runs the simulation, holds UI.
├── requirements.txt        # (ursina)
├── README.md               # This file
└── src/
    ├── __init__.py
    ├── config.py           # All simulation parameters
    ├── simulation.py       # Global state (population/food lists)
    │
    ├── agents/             # Components of the "Organism"
    │   ├── vehicle.py      # The "Body": Holds data, resolves actions
    │   ├── genetics.py     # The "Replicator": Manages genome, mutation
    │   └── behavior.py     # The "Brain": State machine, seeking logic
    │
    └── environment/        # Components of the "World"
        ├── world.py        # The Ground class
        └── resources.py    # The Food class
```

---

## Requirements & How to Run

1.  **Requirements:** This project requires Python 3 and the `ursina` game engine.
    ```bash
    pip install ursina
    ```

2.  **Running the Simulation:**
    ```bash
    python main.py
    ```
    * Use the **Right Mouse Button + WASD** to fly the camera around.
    * Use **Scroll Wheel** to change camera speed.
    * The UI in the top-left corner shows real-time population stats.

---

## How It Works: The Simulation Loop

The simulation runs on two "loops" simultaneously: the **Global Loop** (`main.py`) and the **Agent Loop** (`vehicle.py`).

### 1. The Agent Loop (The "OODA" Loop)

Every frame, every single `Vehicle` runs its `.update()` method, which triggers a full "OODA" (Observe, Orient, Decide, Act) loop:

1.  **Observe (Behavior):** The `behavior.py` module checks the vehicle's `energy` (its internal state) and scans the `simulation.py` lists for nearby food or mates (its external state).
2.  **Orient (Behavior):** The `update_state()` function acts as the "brain," changing the vehicle's `state` attribute to `SEEKING_FOOD`, `SEEKING_MATE`, or `WANDERING` based on its observations.
3.  **Decide (Behavior):** The `perform_action()` function selects the correct movement logic (e.g., `seek_food()`).
4.  **Act (Vehicle):** The vehicle's `position` is updated. If it collides with a target, the `Vehicle` class resolves the action:
    * **Collision with Food:**
        * If another agent is present -> `compete()` is called. The Hawk-Dove ESS logic runs, and energy is distributed.
        * If no one else is present -> `eat()` is called. Energy is gained.
    * **Collision with Mate:** `mate()` is called. `genetics.reproduce()` is run, energy is lost, and a new `Vehicle` is created.
    * **Energy < 0:** `die()` is called. The `Vehicle` is removed from the simulation.

### 2. The Global Loop (The "Accountant")

While the agents are all doing their own thing, the `main.py` `update()` function does two simple jobs:

1.  **Trigger:** It tells every agent to run its Agent Loop (`for v in population: v.update()`).
2.  **Report:** It reads the `simulation.population` list and updates the UI with the current population size and average genetic values.

---

## Key Configurable Parameters

(Found in `src/config.py`)

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `STARTING_POPULATION`| `30` | Number of vehicles at simulation start. |
| `STARTING_FOOD` | `50` | Number of food items in the world. |
| `ENERGY_GAIN_FOOD` | `50.0` | Energy gained from one food item. This is **(V)** in the ESS. |
| `FIGHT_COST` | `80.0` | Energy lost by *both* Hawks in a fight. This is **(C)** in the ESS. |
| `DISPLAY_COST` | `5.0` | Energy lost by Doves (or retreating Hawks) in a conflict. |
| `AGGRESSION_THRESHOLD`| `0.5` | The `aggression` gene value above which a vehicle acts as a Hawk. |
| `MUTATION_RATE` | `0.05` | 5% chance *per gene* to mutate during reproduction. |
| `MUTATION_RATE_META` | `0.01` | 1% chance for the `mutation_multiplier` gene *itself* to mutate. |