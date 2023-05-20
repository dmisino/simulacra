from enum import Enum

import enums
import utils
import llm
from db import db

# Simulations (currently) have 3 main workflow files:
# setup.yaml - Defines steps and prompt templates to initialize a new simulation and entities within it.
# agents.yaml - Defines agents that will run in the simulation. Any entity may be run as an agent, and each agent may have its own workflow yaml file and prompt templates.
# Entity type specific workflow yaml files

def get_path(simulation_type, file):
    return f'simulations/{simulation_type}/{file}'

def replace_tags(text, template_data):
    for key, value in template_data.items():
        text = text.replace(f'{{{key}}}', str(value))
    return text

async def setup_simulation(simulation_type):
    """
    Creates a new simulation and initializes entities as defined in setup.yaml for the given simulation_type
    """
    simulation_id = await process_setup_steps(simulation_type)
    return simulation_id

async def run_simulation(simulation_id):
    """
    Runs agents for all entities in the given simulation
    """
    #TODO: Implement
    return 1

async def process_setup_steps(simulation_type, quiet=False):
    yaml_file = utils.load_yaml_file(get_path(simulation_type, "setup.yaml"))
    steps = yaml_file['steps']
    template_data = {}
    for step in steps:
        if not quiet:
            status = f"Processing step: {step['step_type']}"
            if step['step_type'] == 'PROMPT_ENTITY':
                status += f" ({enums.EntityType[step['entity_type']].name})"
            print(status)
        if step['step_type'] == 'FILE_LOAD':
            # Load file into template_data
            file = step['file']
            text = utils.load_text_file(get_path(simulation_type, file))
            text = replace_tags(text, template_data)
            # For FILE_LOAD steps, the tag name will be the same as the file name without the extension
            tag = file.split('.')[0]
            template_data[tag] = text
        elif step['step_type'] == 'DB_SIMULATION':
            # Create a new simulation in the database
            simulation_id = db.new_simulation(simulation_type)
            template_data["simulation_id"] = simulation_id
        elif step['step_type'] == 'PROMPT_ENTITY':
            # Create a new entity via llm prompt and save to database
            entity_type = step['entity_type']
            entity_type_id = enums.EntityType[entity_type].value
            file = step['file']
            prompt = utils.load_text_file(get_path(simulation_type, file))
            prompt = replace_tags(prompt, template_data)
            llm_results = await llm.get_chat_response_dictionary(prompt)

            """
            Entity prompts should always return a name, summary, and description, though these will be specific to the type of entity. Example response:
            
            world_name: <name>
            world_summary: <summary>
            world_description: <description>
            
            This way the results can be added directly to the template_data dictionary and used in subsequent prompts.
            """
            #print("LLM results: " + str(llm_results))
            llm_name, llm_summary, llm_description = "", "", ""

            # dictionaries are unordered, so we need to iterate through the items to find values
            for llm_key, llm_value in llm_results.items():
                if llm_key.endswith('_name'):
                    llm_name = llm_value
                elif llm_key.endswith('_summary'):
                    llm_summary = llm_value
                elif llm_key.endswith('_description'):
                    llm_description = llm_value
                else:
                    print("Unknown key returned from llm: " + llm_key + " with value: " + llm_value)
                    exit(1)
            
            # Save to database
            simulation_id = template_data["simulation_id"]
            entity_id = db.new_entity(simulation_id, entity_type_id, llm_name, llm_summary, llm_description)

            # Save to template_data
            template_data.update(llm_results)
    return template_data["simulation_id"]