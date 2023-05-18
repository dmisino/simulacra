import json

def format_response(response):
  json_response = json.dumps(response)
  return json_response

def extract_keywords_prompt(input):
  response = '''
  Based on the following input text, extract a comma separated list of keywords that describe the text. Keywords should be any important items, topics, people or categories that are included in or are related to the input text. The keywords should be nouns, verbs, or adjectives. Do not include any prepositions, articles, or other parts of speech that are not nouns, verbs, or adjectives. Keywords should be single words. Include the names of any people mentioned in the input text as keywords. Respond with only one line. Respond only with the list of keywords, not the input text.

  Input text: ''' + input + '''
  '''
  return format_response(response)

def get_random_memories_prompt(count):
  response = '''
  Provide a list of ''' + str(count) + ''' random memories covering many random topics as any typical person would encounter in their daily lives. The memory should be a short phrase or sentence, in past tense, that describes a memory of one of the following: an action, an experience, a conversation, a thought, a realization. The memory should include names of any people involved in that memory.

  Example:

  Went to the store for groceries
  Bought an expensive and fast new car
  Went to a new Italian restaurant with my friend Bob
  Realized that I should focus more on my health
  Started learning to play the guitar
  A scary dog bit me

  Please provide a list of ''' + str(count) + ''' random and varied memories, one per line. Do not number the lines. Respond only like the example.
  '''
  return format_response(response)

def get_random_memories_csv_prompt(count):
  response = '''
  Provide a list of ''' + str(count) + ''' random memories as csv formatted data. Do not include a column header row. The data should cover many random topics as any typical person would encounter in their daily lives. The data should have the following columns: 
  
  memory, keywords
  
  memory should be a short phrase or sentence, in past tense, that describes a memory of one of the following: an action, an experience, a conversation, a thought, a realization. The memory should include specific names of any people involved in that memory.

  keywords should be a comma seperated list of keywords that list any key concepts or things the memory is about. These keywords should be nouns, verbs, or adjectives. Do not include any prepositions, articles, or other parts of speech that are not nouns, verbs, or adjectives. Keywords should be single words. Include the names of any people relevant to the memory as keywords.

  Example:

  "Went to the store for groceries", "store, food, groceries, shopping"
  "Bought an expensive and fast new car", "expensive, money, driving, car"
  "Went to a new Italian restaurant with my friend Bob", "Bob, friend, food, restaurant, Italian"
  "Realized that I should focus more on my health", "health, realization, focus"
  "Started learning to play the guitar","learning, guitar, music"
  "A scary dog bit me","dog, scary, bite"

  Please provide a list of ''' + str(count) + ''' random and varied memories with keywords.
  '''
  return format_response(response)

def get_random_memories_csv_with_categories_prompt(count):
  response = '''
  Provide a list of ''' + str(count) + ''' random memories as csv formatted data. Do not include a column header row. The data should cover many random topics as any typical person would encounter in their daily lives. The data should have the following columns: 
  
  memory, keywords, sports, travel, career, friends, money, health, school, family, entertainment, hobbies, technology, shopping, food, science, animals, danger, adventure, outdoors, music, kids
  
  memory should be a short phrase or sentence, in past tense, that describes a memory of one of the following: an action, an experience, a conversation, a thought, a realization. The memory should include specific names of any people involved in that memory.

  keywords should be a comma seperated list of keywords that list any key concepts or things the memory is about. These keywords should be nouns, verbs, or adjectives. Do not include any prepositions, articles, or other parts of speech that are not nouns, verbs, or adjectives. Keywords should be single words. Include the names of any people relevant to the memory as keywords.

  The other columns should each have a 1 or a 0, to indicate if the memory has anything to do with that specific topic.

  Example:

  "Went to the store for groceries", "store, food, groceries, shopping",0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0
  "Bought an expensive and fast new car", "expensive, money, driving, car",0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0
  "Went to a new Italian restaurant with my friend Bob", "Bob, friend, food, restaurant, Italian",0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0
  "Realized that I should focus more on my health", "health, realization, focus",0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0
  "Started learning to play the guitar","learning, guitar, music",0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0
  "A scary dog bit me","dog, scary, bite",0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0

  Please provide a list of ''' + str(count) + ''' random and varied memories with keywords, and 1 or 0 for each of the other columns as appropriate.
  '''
  return format_response(response)