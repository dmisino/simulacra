# simulacra design doc 

For now I will be using this document as a scratch pad to keep track of thoughts about design while I experiment. It is not complete. It will eventually become an accurate design document.

## Basic concept

The ultimate goal is to get believable and interesting agent behavior and interactions within a dynamic and evolving virtual environment, by creating a flexible and configurable framework that can be implemented for different use cases.

With this in mind, here are a few examples of questions I will seek to answer:

- How much of the overhead of creating and maintaining an evolving virtual environment and the agents within it can be handled by an llm
- How do we handle agent memory and the surfacing of relevant information
- How best to manage a virtual environment such that agents can understand it and navigate or interact with it 
- How best to keep an llm based agent aligned to a plot or premise, from the broadest perspective down to individual actions of agents at every time step, so that the agents appear to do things that are interesting
- What is the balance point between describing every detail of an agents movements vs. just giving broad story narratives
- How can we configure boundary rules so the framework can produce actions and dialog that is useful in various applications

There are many more that come to mind, but as the saying goes "I'll cross that bridge..." 

## Workflows and prompt templates

The intention is for simulations to be configurable via YAML files for processing steps and text files to store prompts specific to each simulation. Ideally different types of simulations could be easily configured by creating new sets of files. 

Each simulation workflow type has its own folder under the /configuration folder. Files:
- setup.yaml
- agent.yaml
- multiple .txt files containing prompt templates as referenced in the yaml files

## Setup workflow step options

- LOAD_FILE
- NEW_SIMULATION
- NEW_ENTITY

## Environment

While initializing a new instance of a simulation, the sandbox environment needs to be created. Initially I will keep this wide open, with prompts to have an llm generate descriptions of a world, and specific places in that world as necessary each with a single paragraph of text. 

Also some mechanism for creating environment trees will be implemented to allow agents to navigate their immediate surroundings and interact with objects, characters, and other running agents.

From this starting point, we will see how much more is needed.

## Agents

After the environment is created, running the simulation will have agents launch into a time step loop, which should be configurable in a YAML file.

Agents should be able to be more than just characters. For example, a world agent operating on an infrequent time step interval could generate new events or changes in the world. A plot agent could generate updates or changes to the story. The framework I envision would allow configuring agents for any defined entity within the simulation, with results that impact the current world state view, story plot, or the memories of any other agent, allowing them to react to what occurs.

There will be a list of pre-defined agent types available, such as NPC, WORLD, PLACE, PLOT, etc. Each agent instance can be configured to use any existing YAML workflow file.

## Agent workflow step options


## Interface

Initially just a command line interface will be available, with simulation and agent messages being fed to the console. I have ideas for generating hooks into graphical framworks, but that will be considered later on.

## Memory stream


## Storage

A db package with all functionality for persistent storage will be included
- sqlite as a backend initially
- database code structured to make implementation of other backends easy