# simulacra
Framework for creating interactive agents with believable behaviors using large language models

## Features
This project is intended to evolve into a framework for creating interactive agents that exhibit believable human behavior and natural interactions with other agents when left to run within a simulation using large language models (LLMs).

**Note, this is early development**. I am mostly concerned with solving certain key challenges before putting it all together as intended. The initial purpose of this project is to iterate on the approach to achieve interesting, realistic and emergent behavior.

The -help option will be kept up to date as I work through things, so run this as described under Usage below to see what you can do.

## Installation and setup

To run this project, you'll need Python installed on your machine. You can install it from [python.org](https://www.python.org/downloads/).

Manual installation of sentence-transformers is required:
```console
pip install -U sentence-transformers
```

## OpenAI API

This project uses the [OpenAI API](https://platform.openai.com/). You will need to get an API key, and to add that to a .env file you create within the project directory. This project includes a .env-sample file, which you can rename to .env, and then add your API key there. 

Alternately you can set the API key in your environment:

```console
rem Windows
set OPENAI_API_KEY=<your api key>

rem Unix or Mac
export OPENAI_API_KEY=<your api key>
```

## Clone the repository

```console
git clone https://github.com/dmisino/simulacra.git
cd simulacra
```

## Usage
```console
python main.py -help
```

## Simulation configuration

Simulations are configured with YAML workflow files and prompt templates. This allows significantly different types of simulations to be configured and run within this framework.

YAML workflow configuration files outline steps for simulation intialization, agent types, agent initialization, agent execution and agent conversations. Steps within YAML workflow files reference the appropriate prompt templates for any steps that will request something from an LLM.

Several pre-configured simulation types will be included. Steps to run them, as well as info for configuring your own will be included here once that code is available.

## Agent prompts

A tentative plan for what would be included in an agent "next action" prompt. I have tested this, but will need to iterate further to get the best results.

- Assistant context. Telling the LLM what their role is.
- World knowledge graph.
- Agent knowledge graph.
- Motivations. What the agent is trying to accomplish. Could be anything from broad goals to a detailed plot outline.
- Current date/time (in the simulation).
- Agent schedule. Necessary to keep the agent aligned during behavior that takes stretches of time, like sleeping.
- Relevant memories. Anything related to the current situation that the agent has encountered previously.
- Recent actions. What the agent has been doing leading up to this moment.
- Environment tree. A detailed breakdown of surroundings.
- "Next action" prompt. Asking the LLM, based on the above info, what the agent does next.

## Relevant memory retrieval

There are different methods available for determining semantic similarity between words, sentances or bodies of text. After testing, for the purposes of an agent retrieving memories, no one method covers all required types of semantic relevance. Due to this, multiple approaches will be used, with top results from each combined into a relevant memory list.

- Sentance similarity. Get memories that mean something similar to the input text.
  - Example
    - Input text: Making food for people when they visit is a great joy
    - Memory:     I love cooking, especially for friends and family
  - Matching implemented with [SBERT](https://arxiv.org/abs/1908.10084), using this [sentance transformer](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) to compare cosine similarity of sentance embeddings.
- Topic relevance. Get memories related to the same main topic, even if the narrative of a memory and the input text are completely different.
  - Example
    - Input text: I am headed to the pet store to pick out a new pet
    - Memory:     I have a fear of dogs since getting bitten as a child
  - Matching implemented by extracting keywords and/or categories, and then comparing word embeddings. Still experimenting with this one.