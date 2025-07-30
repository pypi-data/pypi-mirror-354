def greet_user():
    name = input("Please Enter Your Name: ")
    print(f"Hello Professor. {name}, I am here to help you create exams from a question bank.")
    return name

def ask_to_continue():
    choice = input("\nDo you want me to help you create an exam (Yes to proceed | No to quit the program)? ")
    return choice.strip().lower() == 'yes'

def get_question_bank_path():
    return input("\nPlease Enter the Path to the Question Bank: ")

def get_number_of_questions():
    while True:
        try:
            num = int(input("\nHow many question-answer pairs do you want to include in your exam? "))
            if num > 0:
                return num
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_output_path():
    return input("\nWhere do you want to save your exam? ")

def thank_user(name):
    print(f"\nThank you Professor {name}. Have a good day!")
