from enum import Enum

class SimulationType(Enum):
    fantasy_novel = 1

class EntityType(Enum):
    WORLD = 1
    PLACE = 2
    NPC = 3

class MemoryType(Enum):
    MEMORY = 1,
    REFLECTION = 2,
    DREAM = 3

class WorkflowStepType(Enum):
    LOAD_FILE = 1,
    NEW_SIMULATION = 2
    NEW_ENTITY = 3