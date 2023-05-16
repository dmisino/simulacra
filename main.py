import openai
import os
import sys
from dotenv import load_dotenv
import utils
import prompt

# Load .env settings into environment
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Command line arg is to seed a topic or idea for the story
# seed = ""
# try:
#   n = len(sys.argv)
#   if n > 1:
#     args = sys.argv[1:]
#     seed = " ".join(args)

# except:
#   utils.printError()
#   exit()

# system_prompt = prompt.get_system_prompt()
# create_story_prompt = prompt.get_create_story_prompt(seed)

# total_tokens_used = 0

# print ("\nCreating a new story...\n\n")

# # Create a new book
# messages = [{"role": "system", "content" : system_prompt}]
# messages.append({"role": "user", "content" : create_story_prompt})
# new_book_result = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo", 
#   messages=messages
# )

# # Get info we want out of returned OpenAIObject
# prompt_tokens = new_book_result['usage']['prompt_tokens']
# completion_tokens = new_book_result['usage']['completion_tokens']
# total_tokens = new_book_result['usage']['total_tokens']
# total_tokens_used = total_tokens_used + total_tokens
# response = new_book_result['choices'][0]['message']['content']

# print(utils.print_without_cutting_words(response))

# # Reset messages array to what we need for continuing the story
# user_continue_story_prompt = prompt.get_user_continue_story_prompt()
# messages = [{"role": "system", "content": system_prompt}]
# messages.append({"role": "user", "content": user_continue_story_prompt})
# messages.append({"role": "assistant", "content": response})

# # Loop until story ends
# end = False
# while not end:
#   user_input= ""
#   while user_input not in ["1", "2", "3", "4", "5"]:
#     user_input = input("\nEnter choice number, or 0 to exit: ")
#     if user_input == "0":
#       total_cost = utils.get_openai_gpt35_cost(total_tokens_used)
#       print ("\nUser exited. Total API tokens used: " + str(round(total_tokens_used, 4)) + " (Cost ~$" + str(total_cost) + " USD)\n")
#       exit()
#     elif user_input not in ["1", "2", "3", "4", "5"]:
#       print ("\nInvalid choice. Please select one of the options.")

#   messages.append({"role": "user", "content": user_input})

#   continue_book_result = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo", 
#   messages=messages
#   )

#   # Get info we want out of returned OpenAIObject
#   prompt_tokens = continue_book_result['usage']['prompt_tokens']
#   completion_tokens = continue_book_result['usage']['completion_tokens']
#   total_tokens = continue_book_result['usage']['total_tokens']
#   total_tokens_used = total_tokens_used + total_tokens
#   response = continue_book_result['choices'][0]['message']['content']

#   messages.append({"role": "assistant", "content": response})

#   print("\n" + utils.print_without_cutting_words(response))

#   if "THE END" in response:
#     end = True
    
#     total_cost = utils.get_openai_gpt35_cost(total_tokens_used)
#     print ("\n\nComplete. Total API tokens used: " + str(round(total_tokens_used, 4)) + " (Cost ~$" + str(total_cost) + " USD)\n")