from enums import SimulationType

# Simulations (currently) have 3 main workflow files:
# setup.yaml - Defines steps and prompt templates to initialize a new simulation and entities within it.
# agents.yaml - Defines agents that will run in the simulation. Any entity may be run as an agent, and each agent may have its own workflow yaml file and prompt templates.
# Entity type specific workflow yaml files

def setup_simulation(simulation_type):
    """
    Creates a new simulation and initializes entities as defined in setup.yaml for the given simulation_type
    """
    return 1

def run_simulation(simulation_id):
    """
    Runs agents for all entities in the given simulation
    """
    return 1
