import string
import random
import connection


def get_all_questions(convert_linebreak=False):
    all_questions = connection.get_csv_question_data()

    if convert_linebreak:
        for question in all_questions:
            question["title"] = convert_linebreak_to_br(question["title"])
            question["message"] = convert_linebreak_to_br(question["message"])

    return all_questions


def generate_id():
    rand_letters = random.sample(string.ascii_lowercase, 4)
    id_ = "".join(rand_letters)
    return id_


def convert_linebreak_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))

print(get_all_questions(convert_linebreak=True))














