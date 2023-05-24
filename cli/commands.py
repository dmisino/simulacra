import asyncio
import sys

from common.utils import get_subfolders
from db.datastore import db
import llm.chat_completion as chat_completion
import simulation.workflow as workflow

def verify_workflow(workflow_name):
    if workflow_name in get_subfolders("config"):
        return True
    else:
        print("Unknown simulation workflow: " + workflow_name)
        return False

async def process_commands(args):
    # Process command line args
    n = len(args)
    if n > 0:
        arg = sys.argv[1]
        if arg in ["-help", "-h"]:
            print_help()
        elif arg == "-setup":
            quiet = False
            if n > 1:
                workflow_name = args[1]
            else:
                print ("No simulation workflow specified, see -help for info")
                exit()
            if n > 2:
                if args[2] == "-quiet":
                    quiet = True
            if verify_workflow(workflow_name):
                print("Initializing a new simulation with workflow: " + workflow_name)
                simulation_id = await workflow.run_setup(workflow_name, quiet)
                print("Complete, simulation_id: " + str(simulation_id))
                if not quiet:
                    new_simulation_detail = db.get_simulation_detail(simulation_id) 
                    print(new_simulation_detail)
        elif arg == "-run":
            simulation_id = args[1]
            print("Running agents for simulation_id: " + simulation_id)
            await workflow.run_agents(simulation_id)
        elif arg == "-simulations":
            simulations = db.get_simulations()
            for simulation in simulations:
                print(simulation)
        elif arg == "-simulation":
            simulation_id = args[1]
            simulation = db.get_simulation_detail(simulation_id)
            print(simulation)
        elif arg == "-entities":
            simulation_id = args[1]
            entities = db.get_simulation_entities(simulation_id)
            for entity in entities:
                print(entity)
        elif arg == "-entity":
            entity_id = args[1]
            entity = db.get_entity(entity_id)
            print(entity)
        elif arg == "-memories":
            entity_id = args[1]
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
            entity_id = args[1]
            count = 50
            print("Adding " + str(count) + " random memories for entity_id " + entity_id + "...")
            asyncio.run(chat_completion.add_random_memories(entity_id, count))
            print("Complete")
        elif arg == "-extract_keywords":
            input = args[1]
            print("Extracting keywords from input: '" + input + "'")
            keywords = asyncio.run(chat_completion.extract_keywords(input))
            print("Keywords: " + str(keywords))
        elif arg == "-related":
            entity_id = args[1]
            input = args[2]
            print("Finding memories for entity_id " + entity_id + " related to '" + input + "'")
            limit = 10
            relevant_memories = db.find_relevant_memories_for_entity(entity_id, input, limit)
            for memory in relevant_memories:
                print("Match score: " + str(round(memory[5], 3)) + ", Memory: " + memory[3] + ", Keywords: " + memory[4])
        else:
            print("Unknown command: " + arg + ", see -help for info")
    else:
        print_help()


def print_help():
    print('''
- Items with a * in front of them are not yet implemented/working.
- Included simulation types: fantasy_novel, mini_village. See the README.md for info about setting up a custom simulation.

Commands:
    -help, -h                           Show this help
    -setup <simulation_type>            Create a new simulation
    * -run <simulation_id>              Run a simulation
    -simulations                        Show all initialized simulations
    -simulation <simulation_id>         Show details of a specific simulation
    -entities <simulation_id>           Show all entities for a simulation
    -entity <entity_id>                 Show details of a specific entity
    -memories <entity_id>               Show memories for an entity

Internal function commands:
    -extract_keywords "<input>"         Extract keywords from an input string using an LLM
    -related <entity_id> "<input>"      Get memories most closely related to a list of keywords by comparing embeddings
        
Debug commands:
    -debug_entity                        Create a simulation and sample entity, and show the entity id
    -debug_memories <entity_id>          Add 50 random memories to db for <entity_id>, generated by an LLM
    ''')