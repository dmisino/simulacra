import sqlite3
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import numpy as np
from numpy.linalg import norm
import time

DB_NAME = "simulacra.db"

class db():
    override_db_name = ""

    @staticmethod
    def get_db_conn():
        if db.override_db_name != "":
            database = db.override_db_name
        else:
            database = DB_NAME
        conn = sqlite3.connect(database)
        conn.execute(
            """CREATE TABLE IF NOT EXISTS simulation (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                date            TEXT NOT NULL,
                cycles          INTEGER NOT NULL
                )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS entity (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id   INTEGER NOT NULL REFERENCES simulation (id),
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
                embedding       BLOB NOT NULL,
                date            TEXT NOT NULL
                )"""
        )
        conn.commit()
        return conn

    @staticmethod
    def new_simulation():

        conn = db.get_db_conn()
        cursor = conn.cursor()

        # Insert data into the "simulation" table
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''INSERT INTO simulation (date, cycles)
                        VALUES (?, ?)''', (date, 0))
        
        # Get the last inserted ID
        new_id = cursor.lastrowid

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Return the new ID
        return new_id

    @staticmethod
    def new_entity(simulation_id, name, summary, description):

        conn = db.get_db_conn()
        cursor = conn.cursor()

        # Insert data into the "entity" table
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''INSERT INTO entity (simulation_id, name, summary, description, date)
                        VALUES (?, ?, ?, ?, ?)''', (simulation_id, name, summary, description, date))
        
        # Get the last inserted ID
        new_id = cursor.lastrowid

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Return the new ID
        return new_id

    @staticmethod
    def get_embedding(text):
        model = SentenceTransformer('bert-base-nli-mean-tokens')  # Choose a pre-trained model
        embedding = model.encode([text])
        return embedding[0]

    @staticmethod
    def get_embeddings(memories):
        model = SentenceTransformer('bert-base-nli-mean-tokens')  # Choose a pre-trained model
        embeddings = model.encode(memories)
        return embeddings
    
    @staticmethod
    def save_memory(entity_id, type_id, memory):
        # Get the embedding for the string and convert to bytes
        embedding = db.get_embedding(memory)
        embedding_bytes = embedding.tobytes()
        
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Get connection and save record
        conn = db.get_db_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO memory (entity_id, type_id, memory, embedding, date) VALUES (?, ?, ?, ?, ?)", (entity_id, type_id, memory, embedding_bytes, date))
        conn.commit()
        conn.close()

    @staticmethod
    def save_memories(entity_id, type_id, memories):
        conn = db.get_db_conn()
        cursor = conn.cursor()        
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        start_time = time.time()
        print("getting embeddings")
        embeddings = db.get_embeddings(memories)
        end_time = time.time()
        print("getting embeddings complete, time: " + str(end_time - start_time))

        data = []
        i = 0
        print("preparing data")
        for memory in memories:
            embedding_bytes = embeddings[i].tobytes()
            data.append((entity_id, type_id, memory, embedding_bytes, date))
            i += 1
        query = "INSERT INTO memory (entity_id, type_id, memory, embedding, date) VALUES (?, ?, ?, ?, ?)"
        print("preparing data complete")
        # Execute the query with executemany()
        cursor.executemany(query, data)

        conn.commit()
        conn.close()

    # Find closest matching memories based on cosine similarity of embeddings
    @staticmethod
    def resize_embedding(embedding, target_dim):
        current_dim = embedding.shape[0]
        if current_dim == target_dim:
            return embedding
        resized_embedding = np.interp(np.linspace(0, 1, target_dim), np.linspace(0, 1, current_dim), embedding)
        return resized_embedding

    @staticmethod
    def find_relevant_memories_for_entity(entity_id, input_string, limit):
        input_embedding = db.get_embedding(input_string)

        # Get connection and retrieve relevant columns from memory table
        conn = db.get_db_conn()
        cursor = conn.cursor()    
        cursor.execute("SELECT id, entity_id, type_id, memory, embedding FROM memory WHERE entity_id = ?", (entity_id,))
        rows = cursor.fetchall()

        # Calculate cosine similarity for each row and populate similarity column
        new_rows = []
        for row in rows:
            row_embedding = np.frombuffer(row[4], dtype=np.float64)
            resized_input_embedding = db.resize_embedding(input_embedding, row_embedding.shape[0])
            similarity = cosine_similarity([resized_input_embedding], [row_embedding])[0][0]
            new_row = row[:4] + (similarity,)
            new_rows.append(new_row)

        # Sort the rows based on cosine similarity
        sorted_rows = sorted(new_rows, key=lambda x: x[4], reverse=True)

        # Return the limited number of similar rows with relevant columns
        return sorted_rows[:limit]