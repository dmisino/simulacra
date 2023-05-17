from db import db
from prompt import get_random_memories_prompt, extract_keywords_prompt
import openai
from utils import csv_string_to_array
import asyncio

async def llm(prompt):
    messages = [{"role": "user", "content" : prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages
    )
    result = response['choices'][0]['message']['content']
    return result

async def extract_keywords(input):
    prompt = extract_keywords_prompt(input)
    return await llm(prompt)

async def add_random_memories(entity_id, count):
    prompt = get_random_memories_prompt(count)
    response = await llm(prompt)
    
    # response should be a csv fomatted list with 2 columns: memory, keywords
    memories = csv_string_to_array(response)
    db.save_memories(entity_id, 1, memories)