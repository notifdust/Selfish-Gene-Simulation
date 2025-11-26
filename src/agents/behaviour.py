from ursina import *
import random
from src import config
from src import simulation # Import global lists

def update_state(vehicle):
    """Simple state machine. Called by the vehicle every frame."""
    if vehicle.energy < 0:
        vehicle.die()
        return

    if vehicle.energy > config.REPRODUCE_ENERGY_THRESHOLD:
        vehicle.state = "SEEKING_MATE"
    elif vehicle.energy < config.HUNGER_THRESHOLD:
        vehicle.state = "SEEKING_FOOD"
    else:
        vehicle.state = "WANDERING"

def perform_action(vehicle):
    """Routes to the correct action based on the vehicle's state."""
    if vehicle.state == "SEEKING_FOOD":
        seek_food(vehicle)
    elif vehicle.state == "SEEKING_MATE":
        seek_mate(vehicle)
    else: # "WANDERING"
        wander(vehicle)

def find_target(vehicle, target_list):
    """Finds the closest target in a list within vision range."""
    closest_target = None
    min_dist = vehicle.vision

    for item in target_list:
        if item == vehicle or not item.enabled: # Don't target self or disabled
            continue
        dist = distance(vehicle, item)
        if dist < min_dist:
            min_dist = dist
            closest_target = item
    
    return closest_target

def wander(vehicle):
    """Move randomly."""
    if random.random() < 0.1: # 10% chance to turn
        vehicle.rotation_y += random.uniform(-30, 30)
    
    vehicle.position += vehicle.forward * vehicle.speed * time.dt
    # Keep within world bounds
    vehicle.position = (
        clamp(vehicle.position.x, -config.WORLD_SIZE/2, config.WORLD_SIZE/2),
        vehicle.position.y,
        clamp(vehicle.position.z, -config.WORLD_SIZE/2, config.WORLD_SIZE/2)
    )

def seek_food(vehicle):
    if not vehicle.target or not vehicle.target.enabled:
        vehicle.target = find_target(vehicle, simulation.food_items)

    if vehicle.target:
        vehicle.look_at(vehicle.target)
        vehicle.position += vehicle.forward * vehicle.speed * time.dt
        
        # Check for collision with food
        if distance(vehicle, vehicle.target) < 1.0:
            vehicle.eat(vehicle.target) # Call the Vehicle's eat method
    else:
        wander(vehicle) # No food in sight, wander

def seek_mate(vehicle):
    if not vehicle.target or not vehicle.target.enabled:
        vehicle.target = find_target(vehicle, simulation.population)

    if vehicle.target and vehicle.target.state == "SEEKING_MATE":
        vehicle.look_at(vehicle.target)
        vehicle.position += vehicle.forward * vehicle.speed * time.dt

        if distance(vehicle, vehicle.target) < 1.0:
            vehicle.mate(vehicle.target) # Call the Vehicle's mate method
    else:
        wander(vehicle) # No mates in sight, wander