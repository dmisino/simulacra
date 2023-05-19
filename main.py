import asyncio
import os
import sys

import openai
from dotenv import load_dotenv

from db import db
from enums import SimulationType
import llm
from models import Entity, Memory, Simulation
import simulation
import utils

# Load .env settings into environment
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

if os.getenv('OPENAI_API_KEY') == None:
    print("OPENAI_API_KEY not set in environment. See README.md for info.")
    sys.exit()

# Process command line args
n = len(sys.argv)
if n > 1:
    arg = sys.argv[1]
    if arg in ["-help", "-h"]:
        utils.print_help()
    elif arg == "-setup":
        simulation_type = sys.argv[2]
        if simulation_type not in SimulationType.__members__:
            print("Unknown simulation type: " + simulation_type)
        else:
            print("Initializing a new simulation of type: " + simulation_type)
            simulation_id = simulation.setup_simulation(simulation_type)
            #simulation = db.get_simulation_detail(simulation_id)
            print("Complete")
            #print(simulation)
    elif arg == "-run":
        simulation_id = sys.argv[2]
        print("Not implemented yet")
    #     print("Running simulation_id: " + simulation_id)
    #     simulation = db.get_simulation(simulation_id)
    #     simulation.run()
    elif arg == "-simulations":
        simulations = db.get_simulations()
        for simulation in simulations:
            print(simulation)
    elif arg == "-simulation":
        simulation_id = sys.argv[2]
        simulation = db.get_simulation_detail(simulation_id)
        print(simulation)
    elif arg == "-entities":
        simulation_id = sys.argv[2]
        entities = db.get_simulation_entities(simulation_id)
        for entity in entities:
            print(entity)
    elif arg == "-entity":
        entity_id = sys.argv[2]
        entity = db.get_entity(entity_id)
        print(entity)
    elif arg == "-memories":
        entity_id = sys.argv[2]
        memories = db.get_entity_memories(entity_id)
        for memory in memories:
            print(memory)

    # DEBUG commands ##########################################
    elif arg == "-debug_entity":
        simulation_id = db.new_simulation()
        name = "Bob"
        summary = "Bob is a test entity."
        description = "Bob is a test entity who will get lots of random memories."
        entity_id = db.new_entity(simulation_id, name, summary, description)
        print("Complete, simulation_id: " + str(simulation_id) + ", entity_id: " + str(entity_id))
    elif arg == "-debug_memories":
        entity_id = sys.argv[2]
        count = 50
        print("Adding " + str(count) + " random memories for entity_id " + entity_id + "...")
        asyncio.run(llm.add_random_memories(entity_id, count))
        print("Complete")
    elif arg == "-extract_keywords":
        input = sys.argv[2]
        print("Extracting keywords from input: '" + input + "'")
        keywords = asyncio.run(llm.extract_keywords(input))
        print("Keywords: " + str(keywords))
    elif arg == "-related":
        entity_id = sys.argv[2]
        input = sys.argv[3]
        print("Finding memories for entity_id " + entity_id + " related to '" + input + "'")
        limit = 10
        relevant_memories = db.find_relevant_memories_for_entity(entity_id, input, limit)
        for memory in relevant_memories:
            print("Match score: " + str(round(memory[5], 3)) + ", Memory: " + memory[3] + ", Keywords: " + memory[4])
    else:
        print("Unknown command: " + arg)