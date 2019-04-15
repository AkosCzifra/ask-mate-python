import string
import random
import connection


def get_all_questions():
    all_questions = connection.get_csv_question_data()
    return all_questions


def generate_id():
    rand_letters = random.sample(string.ascii_lowercase, 4)
    id_ = "".join(rand_letters)
    return id_















