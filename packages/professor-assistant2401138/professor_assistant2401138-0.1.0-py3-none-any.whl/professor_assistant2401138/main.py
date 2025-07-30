from .interaction import (
    greet_user, ask_to_continue, get_question_bank_path,
    get_number_of_questions, get_output_path, thank_user
)
from .fileHandler import read_question_bank, write_exam
from .qsnCreator import create_exam

def main():
    print("Welcome to professor assistant version 1.0.")
    name = greet_user()

    while ask_to_continue():
        qsn_path = get_question_bank_path()
        questions = read_question_bank(qsn_path)
        if not questions:
            continue

        num_qsn = get_number_of_questions()
        out_path = get_output_path()
        success = create_exam(questions, num_qsn, out_path)

        if success:
            print(f"\nCongratulations Professor {name}. Your exam is created and saved in {out_path}.")
        else:
            print("Failed to create the exam.")

    thank_user(name)
