# simulacra
Framework for creating interactive agents with believable behaviors using large language models

## Features
This project is intended to become a framework for creating interactive agents that exhibit believable human behavior and natural interactions with other agents when left to run within a simulation by using large language models (LLMs).

Note, this is early development. I am mostly concerned with solving certain key challenges before putting it all together as intended. 

One of the tricky aspects of creating agents with believable behavior is surfacing memories that are most relevant to any given situation, so the LLM can be provided with the background information it should consider in creating an agents "next action" response. 

One solution is to utilize a language model and feed it a list of agent memories and a description of the current situation and ask it which memories are relevant. This works for very limited applications, but it is not practical once you have large numbers of memories. I am experimenting with using embeddings of extracted keywords as a method to surface relevant memories. Once this is working as required, I can add other aspects that are important to generating an agents memory space. 

My current understanding is that an effective algorithm to surface agent memories should include the following considerations:
- Relevancy of memories to the current situation
- Memory recency
- Overall importance or impact the memory had on the agent
- Reflection, or creating new ideas by thinking about past experiences
- Dreams (Optional), similar to reflections, but more random and imaginative

Along with the memory space, other key information will need to be included in prompting an LLM to decide an agents next action such as:
- Agent, world and environment knowledge graphs
- Detailed environment trees to allow interaction with objects
- Agent motivations, goals, or a plot outline guiding overall behavior
- Mundane functional needs (eating, sleeping, dressing)
- Knowledge of other agents in their vicinity
- Daily activity cycles
- A method to sync agent actions when they interact
- etc.

The point of this project is to iterate on the elements that lead to interesting, emergent and realistic behavior. From there we will likely need some method for constraining agent behavior with configurable rules, so the framework can produce whatever is required for any specific application.

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