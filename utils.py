import csv
import os
from io import StringIO
import sys
import string

def strip_non_letters(text):
    """
    Remove non-letter characters from the beginning, and 
    whitespace from the end of a string
    """    
    formatted_text = text.lstrip(string.punctuation + string.whitespace)
    formatted_text = formatted_text.rstrip(string.whitespace)
    return formatted_text

def console_output(switch):
    """
    Turn console output on or off
    """
    if switch == 0:
        sys.stdout = open(os.devnull, 'w') # Turn off console output
    else:
        sys.stdout = sys.__stdout__ # Turn on console output
    

def get_openai_gpt35_cost(total_tokens):
    total_cost = total_tokens/1000 * 0.002
    return total_cost

def print_without_cutting_words(text):
    cols, rows = os.get_terminal_size()
    text = text.rstrip('\n')  # Remove any trailing newline character
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        line_length = 0
        new_line = []
        for word in line.split():
            if not word:
                continue
            word_length = len(word)
            if line_length + word_length + 1 <= cols:
                new_line.append(word)
                line_length += word_length + 1
            else:
                new_lines.append(' '.join(new_line))
                new_line = [word]
                line_length = word_length
            new_lines.append(' '.join(new_line))
    return '\n'.join(new_lines)

def read_file_to_array(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines

def csv_string_to_array(string):
    a = []
    with StringIO(string) as file:
        for line in file:
            values = line.split('", "')
            a.append([values[0].strip().replace('"', ''), values[1].strip().replace('"', '')])
    return a