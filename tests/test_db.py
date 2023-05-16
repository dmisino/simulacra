from db import *
from utils import *
import unittest
import sqlite3
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

DB_NAME = "test_simulacra.db"

class TestDbFunctions(unittest.TestCase):

    simulation_id = 0
    entity_id = 0

    @classmethod
    def setUpClass(cls):
        db.override_db_name = DB_NAME

        # Insert data into the "simulation" table
        new_id = db.new_simulation()
        TestDbFunctions.simulation_id = new_id

        # Insert data into the "entity" table
        name = "Bob"
        summary = "Bob is a test entity."
        description = "Bob is a test entity who will get lots of random memories."
        TestDbFunctions.entity_id = db.new_entity(TestDbFunctions.simulation_id, name, summary, description)

        # Insert data into the "memory" table
        print("reading test file")
        test_memories = read_file_to_array("tests/test_memories.txt")
        print("saving test memories")
        db.save_memories(TestDbFunctions.entity_id, 1, test_memories)
        print("saving test memories complete")

    @classmethod
    def tearDownClass(cls):
        os.remove(DB_NAME)
        db.override_db_name = ""

    def test_get_db_conn(self):
        # Test if the database connection is returned successfully
        conn = db.get_db_conn()
        self.assertIsNotNone(conn)
        conn.close()

    def test_save_memory(self):
        # Test if the memory is saved correctly in the database
        test_string = "This is a single test memory."
        db.save_memory(TestDbFunctions.entity_id, 1, test_string)

        # Retrieve the saved memory from the database
        conn = db.get_db_conn()
        cursor = conn.cursor()  
        cursor.execute("SELECT * FROM memory WHERE memory=?", (test_string,))
        result = cursor.fetchone()
        conn.close()

        # Check if the retrieved memory matches the saved memory
        self.assertIsNotNone(result)
        self.assertEqual(result[3], test_string)

    def test_find_relevant_memories_for_entity(self):

        # Test finding relevant memories
        input_string = "space"
        limit = 20
        relevant_memories = db.find_relevant_memories_for_entity(TestDbFunctions.entity_id, input_string, limit)
        for memory in relevant_memories:
            print("Relevant memory: " + str(memory[4]) + ", " + memory[3])

        # Check if the correct number of relevant memories is returned
        self.assertEqual(len(relevant_memories), limit)

        # Check if the relevant memories are ordered by similarity




if __name__ == '__main__':
    unittest.main()
