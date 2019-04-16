import string
import random
import connection


def get_all_questions(convert_linebreak=False):
    all_questions = connection.get_csv_question_data(connection.QUESTION_CSV_PATH)

    if convert_linebreak:
        for question in all_questions:
            question["title"] = convert_linebreak_to_br(question["title"])
            question["message"] = convert_linebreak_to_br(question["message"])

    return all_questions


def get_all_answers(convert_linebreak=False):
    all_answers = connection.get_csv_question_data(connection.ANSWER_CSV_PATH)

    if convert_linebreak:
        for question in all_answers:
            question["message"] = convert_linebreak_to_br(question["message"])
    return all_answers


def convert_linebreak_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))


def get_all_answers_by_question_id(question_id):
    answers = get_all_answers(True)
    filtered_answers = []
    for answer in answers:
        if answer["question_id"] == question_id:
            filtered_answers.append(answer)
    return filtered_answers


def generate_id(length=4):
    rand_letters = random.sample(string.ascii_lowercase, length)
    id_ = "".join(rand_letters)
    return id_














