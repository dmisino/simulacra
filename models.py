from enum import Enum

import enums

class Simulation:
    def __init__(self, id, workflow, date, cycles):
        self.id = id
        self.workflow = workflow
        self.date = date
        self.cycles = cycles

    def __repr__(self):
        s = f'''
Simulation
id: {self.id}
workflow: {self.workflow}
date: {self.date}
cycles: {self.cycles}
'''
        return s

class Entity:
    def __init__(self, id, simulation_id, type_id, name, summary, description, date):
        self.id = id
        self.simulation_id = simulation_id
        self.type_id = type_id
        self.name = name
        self.summary = summary
        self.description = description
        self.date = date

    def __repr__(self):
        s = f'''
Entity
id: {self.id}
simulation_id: {self.simulation_id}
type_id: {self.type_id} ({enums.EntityType(self.type_id).name})
name: {self.name}
summary: {self.summary}
description: {self.description}
'''
        return s

class Memory:
    def __init__(self, id, entity_id, type_id, memory, keywords, embedding, date):
        self.id = id
        self.entity_id = entity_id
        self.type_id = type_id
        self.memory = memory
        self.keywords = keywords
        self.embedding = embedding
        self.date = date

    def __repr__(self):
        s = f'''
Memory
id: {self.id}
entity_id: {self.entity_id}
type_id: {self.type_id} ({enums.MemoryType(self.type_id).name})
memory: {self.memory}
keywords: {self.keywords}
date: {self.date}
'''
        return s
    
class SimulationDetail:
    def __init__(self, id, workflow, date, cycles, entities):
        self.id = id
        self.workflow = workflow
        self.date = date
        self.cycles = cycles
        self.entities = entities

    def __repr__(self):
        s = f'''
Simulation
id: {self.id}
workflow: {self.workflow}
date: {self.date}
cycles: {self.cycles}
'''
        for entity in self.entities:
            s += f'''
Entity
id: {entity.id}
type_id: {entity.type_id} ({enums.EntityType(entity.type_id).name})
name: {entity.name}
summary: {entity.summary}
description: {entity.description}
'''
        return s