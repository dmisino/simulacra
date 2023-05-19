from enum import Enum

import enums
import utils
from db import db

# Simulations (currently) have 3 main workflow files:
# setup.yaml - Defines steps and prompt templates to initialize a new simulation and entities within it.
# agents.yaml - Defines agents that will run in the simulation. Any entity may be run as an agent, and each agent may have its own workflow yaml file and prompt templates.
# Entity type specific workflow yaml files

def get_path(simulation_type, file):
    return f'simulations/{simulation_type}/{file}'

def replace_tags(text, template_data):
    for key, value in template_data.items():
        text = text.replace(f'{{{key}}}', value)
    return text

def setup_simulation(simulation_type):
    """
    Creates a new simulation and initializes entities as defined in setup.yaml for the given simulation_type
    """
    process_setup_steps(simulation_type)

def run_simulation(simulation_id):
    """
    Runs agents for all entities in the given simulation
    """
    #TODO: Implement
    return 1

def process_setup_steps(simulation_type):
    yaml_file = utils.load_yaml_file(get_path(simulation_type, "setup.yaml"))
    steps = yaml_file['steps']
    template_data = {}
    for step in steps:
        if step['step_type'] == 'LOAD_FILE':
            # Load file into template_data
            file = step['file']
            text = utils.load_text_file(get_path(simulation_type, file))
            text = replace_tags(text, template_data)
            output = step['output']
            for item in output:
                name = item['name']
                alias = item.get('alias')
                tag = alias if alias else name
                template_data[tag] = text
        elif step['step_type'] == 'NEW_SIMULATION':
            # Create a new simulation in the database
            simulation_id = db.new_simulation(simulation_type)
            template_data["simulation_id"] = simulation_id
        elif step['step_type'] == 'CREATE_ENTITY':
            entity_type = step['entity_type']
            entity_type_id = enums.EntityType[entity_type].value
            file = step['file']
            prompt = utils.load_text_file(get_path(simulation_type, file))
            prompt = replace_tags(prompt, template_data)
            # Call llm to generate entity

            
            # Result items
            # 1. name
            # 2. summary
            # 3. description
            name = ""
            summary = ""
            description = ""

            
            # # Save to database
            # simulation_id = template_data['simulation_id']
            # entity_id = db.new_entity(simulation_id, entity_type_id, name, summary, description)

            # # Save to template_data
            # output = step['output']
            # for item in output:
            #     name = item['name']
            #     alias = item.get('alias')
            #     tag = alias if alias else name
            #     template_data[tag] = 
            


