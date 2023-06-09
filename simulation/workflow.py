from enum import Enum

import common.enums as enums
import common.utils as utils
import llm.chat_completion as chat_completion
from db.datastore import db

# Simulations (currently) have 3 main workflow files:
# setup.yaml - Defines steps and prompt templates to initialize a new simulation and entities within it.
# agents.yaml - Defines agents that will run in the simulation. Any entity may be run as an agent, and each agent may have its own workflow yaml file and prompt templates.
# Entity type specific workflow yaml files

def get_path(workflow_type, file):
    return f'config/{workflow_type}/{file}'

def replace_tags(text, template_data):
    for key, value in template_data.items():
        text = text.replace(f'{{{key}}}', str(value))
    return text

async def run_setup(workflow_type, quiet=False):
    """
    Creates a new simulation and initializes entities as defined in setup.yaml for the given simulation_type
    """
    simulation_id = await process_setup(workflow_type, quiet)
    return simulation_id

async def run_agents(simulation_id, quiet=False):
    """
    Runs agents for the specified simulation
    """
    await process_agents(simulation_id, quiet)

async def process_agents(simulation_id, quiet=False):
    simulation = db.get_simulation(simulation_id)
    yaml_file = utils.load_yaml_file(get_path(simulation.workflow, "agents.yaml"))
    print(f"loaded yaml file {simulation.workflow}/agents.yaml")
    time_step = yaml_file['time_step']
    print(f"time_step: {time_step}")
    agents = yaml_file['agents']
    for agent in agents:
        agent_name = agent['name']
        agent_type = agent['agent_type']
        print(f"Agent Name: {agent_name}")
        print(f"Agent Type: {agent_type}")

        # Loop through step nodes
        steps = agent['steps']
        for step in steps:
            step_name = step['name']
            step_type = step['step_type']
            interval = step['interval']
            files = step['file']
            print(f"\tStep Name: {step_name}")
            print(f"\tStep Type: {step_type}")
            print(f"\tInterval: {interval}")
            print(f"\tFile: {file}")
        print()  # Add a newline between agents
    return 1

async def process_setup(workflow_type, quiet=False):
    yaml_file = utils.load_yaml_file(get_path(workflow_type, "setup.yaml"))
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
            text = utils.load_text_file(get_path(workflow_type, file))
            text = replace_tags(text, template_data)
            # For FILE_LOAD steps, the tag name will be the same as the file name without the extension
            tag = file.split('.')[0]
            template_data[tag] = text
        elif step['step_type'] == 'DB_SIMULATION':
            # Create a new simulation in the database
            simulation_id = db.new_simulation(workflow_type)
            template_data["simulation_id"] = simulation_id
        elif step['step_type'] == 'PROMPT_ENTITY':
            # Create a new entity via llm prompt and save to database
            entity_type = step['entity_type']
            entity_type_id = enums.EntityType[entity_type].value
            file = step['file']
            prompt = utils.load_text_file(get_path(workflow_type, file))
            prompt = replace_tags(prompt, template_data)
            llm_results = await chat_completion.get_chat_response_dictionary(prompt)

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