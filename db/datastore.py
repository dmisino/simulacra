import inspect
import os
import sqlite3
from datetime import datetime

import numpy as np

import common.utils as utils
import db.embedding as embedding
from common.models import Entity, Memory, Simulation, SimulationDetail

DB_NAME = "simulacra.db"

class db():
    override_db_name = ""

    @staticmethod
    def get_db_conn():
        try:
            if db.override_db_name != "":
                database = db.override_db_name
            else:
                database = DB_NAME
            conn = sqlite3.connect(database)
            conn.execute(
                """CREATE TABLE IF NOT EXISTS simulation (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow        TEXT NOT NULL,
                    date            TEXT NOT NULL,
                    cycles          INTEGER NOT NULL
                    )"""
            )
            conn.execute(
                """CREATE TABLE IF NOT EXISTS entity (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    simulation_id   INTEGER NOT NULL REFERENCES simulation (id),
                    type_id         INTEGER NOT NULL,
                    name            TEXT NOT NULL,
                    summary         TEXT NOT NULL,
                    description     TEXT NOT NULL,
                    date            TEXT NOT NULL
                    )"""
            )
            conn.execute(
                """CREATE TABLE IF NOT EXISTS memory (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_id       INTEGER NOT NULL REFERENCES entity (id),
                    type_id         INTEGER NOT NULL,
                    memory          TEXT NOT NULL,
                    keywords        TEXT NOT NULL,
                    embedding       BLOB NOT NULL,
                    date            TEXT NOT NULL
                    )"""
            )
            conn.commit()
            return conn
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)

    @staticmethod
    def delete_db_file():
        try:
            if db.override_db_name != "":
                database = db.override_db_name
            else:
                database = DB_NAME
            if os.path.exists(database):
                os.remove(database)
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)          

    @staticmethod
    def get_simulations():
        try:
            conn = db.get_db_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, workflow, date, cycles FROM simulation ORDER BY cycles DESC, date DESC")
            rows = cursor.fetchall()
            simulations = [Simulation(*row) for row in rows]
            conn.close()
            return simulations
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e) 

    @staticmethod
    def new_simulation(workflow):
        try:
            conn = db.get_db_conn()
            cursor = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''INSERT INTO simulation (workflow, date, cycles) VALUES (?, ?, ?)''', (workflow, date, 0))
            simulation_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return simulation_id
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)  

    @staticmethod
    def get_simulation(simulation_id):
        try:
            conn = db.get_db_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, workflow, date, cycles FROM simulation WHERE id = ?", (simulation_id,))
            row = cursor.fetchone()
            simulation = Simulation(*row)
            conn.close()
            return simulation
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)

    def get_simulation_entities(simulation_id):
        try:
            conn = db.get_db_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, simulation_id, type_id, name, summary, description, date FROM entity WHERE simulation_id = ?", (simulation_id,))
            rows = cursor.fetchall()
            entities = [Entity(*row) for row in rows]
            conn.close()
            return entities
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)
    
    def get_simulation_detail(simulation_id):
        try:
            simulation = db.get_simulation(simulation_id)
            entities = db.get_simulation_entities(simulation_id)
            simulation_detail = SimulationDetail(simulation_id, simulation.workflow, simulation.date, simulation.cycles, entities)
            return simulation_detail
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)

    @staticmethod
    def new_entity(simulation_id, entity_type_id, name, summary, description):
        try:
            conn = db.get_db_conn()
            cursor = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''INSERT INTO entity (simulation_id, type_id, name, summary, description, date) VALUES (?, ?, ?, ?, ?, ?)''', (simulation_id, entity_type_id, name, summary, description, date))
            entity_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return entity_id
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)
        
    @staticmethod
    def get_entity(entity_id):
        try:
            conn = db.get_db_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, simulation_id, type_id, name, summary, description, date FROM entity WHERE id = ?", (entity_id,))
            row = cursor.fetchone()
            entity = Entity(*row)
            conn.close()
            return entity
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)    

    @staticmethod
    def get_entity_memories(entity_id):
        try:
            conn = db.get_db_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, memory, keywords FROM memory WHERE entity_id = ?", (entity_id,))
            memories = cursor.fetchall()
            conn.close()
            return memories
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)    
            
    @staticmethod
    def save_memory(entity_id, type_id, memory):
        try:
            keywords = utils.remove_stop_words(memory)
            embedding = db.get_embedding(memory)
            embedding_bytes = embedding.tobytes()
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = db.get_db_conn()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO memory (entity_id, type_id, memory, keywords, embedding, date) VALUES (?, ?, ?, ?, ?, ?)", (entity_id, type_id, memory, keywords, (sqlite3.Binary(embedding_bytes),), date))
            conn.commit()
            conn.close()
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)
        
    @staticmethod
    def save_memories(entity_id, type_id, memories):
        try:
            conn = db.get_db_conn()
            cursor = conn.cursor()        
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            keywords = []
            for memory in memories:
                keywords.append(utils.remove_stop_words(memory).lower())
            embeddings = db.get_embeddings(memories)
            data = []
            i = 0
            for memory in memories:
                embedding_bytes = embeddings[i].tobytes()
                data.append((entity_id, type_id, memory, keywords[i], (sqlite3.Binary(embedding_bytes),), date))
                i += 1
            query = "INSERT INTO memory (entity_id, type_id, memory, keywords, embedding, date) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.executemany(query, data)
            conn.commit()
            conn.close()
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)
        
    @staticmethod
    def find_relevant_memories_for_entity(entity_id, input_string, limit):
        """
        Find closest matching memories based on cosine similarity of embeddings
        """
        try:
            input_embedding = db.get_embedding(utils.remove_stop_words(input_string))
            conn = db.get_db_conn()
            cursor = conn.cursor()    
            cursor.execute("SELECT id, entity_id, type_id, memory, keywords, embedding FROM memory WHERE entity_id = ?", (entity_id,))
            rows = cursor.fetchall()

            # Calculate cosine similarity for each row and populate similarity column
            new_rows = []
            for row in rows:
                row_embedding = np.frombuffer(row[5], dtype=np.float64)
                row_embedding = row_embedding.reshape((-1,))
                similarity = embedding.get_similarity([input_embedding], [row_embedding])[0][0]
                new_row = row[:5] + (similarity,)
                new_rows.append(new_row)

            # Sort rows based on cosine similarity
            sorted_rows = sorted(new_rows, key=lambda x: x[5], reverse=True)
            return sorted_rows[:limit]
        except Exception as e:
            utils.print_error(inspect.currentframe().f_code.co_name, e)        