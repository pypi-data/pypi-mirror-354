import random
from .fileHandler import write_exam

def create_exam(questions, number, output_path):
    if number > len(questions):
        print("Error: Not enough questions in the question bank.")
        return False
    selected = random.sample(questions, number)
    return write_exam(selected, output_path)
