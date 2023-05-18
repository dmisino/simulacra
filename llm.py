import asyncio

import openai

from db import db
from prompt import extract_keywords_prompt, get_random_memories_prompt
from utils import strip_non_letters


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
    memories = response.splitlines()
    memories = [strip_non_letters(memory) for memory in memories]
    db.save_memories(entity_id, 1, memories)