import inspect

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import common.utils as utils

TRANSFORMER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_embedding(text):
    """
    Get an embedding for a string
    """
    try:
        model = SentenceTransformer(TRANSFORMER_MODEL)
        embedding = model.encode([text])
        return embedding[0]
    except Exception as e:
        utils.print_error(inspect.currentframe().f_code.co_name, e)
    
def get_embeddings(text_array):
    """
    Get embeddings for an array of strings
    """
    try:
        model = SentenceTransformer(TRANSFORMER_MODEL)
        embeddings = model.encode(text_array)
        return embeddings
    except Exception as e:
        utils.print_error(inspect.currentframe().f_code.co_name, e)

def get_similarity(embedding1, embedding2):
    """
    Get the cosine similarity between two embeddings
    """
    try:
        return cosine_similarity([embedding1], [embedding2])[0][0]
    except Exception as e:
        utils.print_error(inspect.currentframe().f_code.co_name, e)