import os  # Import the os module to work with file paths and directories

# this function checks if a file exists in a given folder with the exact uppercase/lowercase letters
def check_caseSensitivity(path):  # Define a function that takes a file path as input
    folder, filename = os.path.split(path)  # Separate folder and filename from the path
    if folder == '':  # If no folder is specified in the path
        folder = '.'  # Use the current directory ('.') as the folder

    try:
        files = os.listdir(folder)  # List all files in the specified folder
    except FileNotFoundError:  # If the folder does not exist
        return False, "Directory does not exist."  # Return False with an error message

    for x in files:  # Loop through all files in the folder
        if x == filename:  # If a file with the exact same name and case is found
            return True, ""  # Return True and an empty message (success)
    return False, "File name does not match."  # If filename exists but case doesn't match, return error

def read_question_bank(path):  #  function to read questions from a file
    check_case, msg = check_caseSensitivity(path)  # Check if the file exists with the correct case
    if not check_case:  # If the case is not correct
        print(f"Error: {msg} Please check the exact file path/casing and try again.")  # Print an error message
        return None  # Stop the function and return None

    try:
        with open(path, 'r', encoding='utf-8') as file:  # Try to open the file in read mode with UTF-8 encoding
            lines = file.readlines()  # Read all lines from the file into a list
            questions = []  # Create an empty list to store questions and answers

            for i in range(0, len(lines) - 1, 2):  # Loop through the lines, two at a time (question + answer)
                question = lines[i].strip()  # Remove spaces and newline from the question line
                answer = lines[i + 1].strip()  # Remove spaces and newline from the answer line
                questions.append((question, answer))  # Add the question-answer pair to the list
            return questions  # Return the list of question-answer pairs
    except FileNotFoundError:  # If the file is not found

        print("Error: File not found. Please check the path and try again.")  # Print an error message
        return None  # Return None to indicate failure

# Function to write a list of question-answer pairs to an output file
def write_exam(questions, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:# Open the output file in write mode with UTF-8 encoding
           
            for i, (q, a) in enumerate(questions, 1): # Loop through each (question, answer) tuple with an index starting at 1
                f.write(f"Q{i}: {q}\nA{i}: {a}\n\n") # Write the question and answer in formatted form
        return True
    
    
    except Exception as e:# Catch any error during file writing and print the message
        print(f"Error writing exam file: {e}")
        return False  