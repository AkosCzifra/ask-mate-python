import csv
import os


QUESTION_CSV = 'question.csv'
ANSWER_CSV = 'answer.csv'
QUESTION_CSV_PATH = os.getenv('QUESTION_CSV_PATH') if 'QUESTION_CSV_PATH' in os.environ else QUESTION_CSV
ANSWER_CSV_PATH = os.getenv('ANSWER_CSV_PATH') if 'ANSWER_CSV_PATH' in os.environ else ANSWER_CSV
QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADER = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_csv_question_data(one_question_id=None):
    user_questions = []
    with open (QUESTION_CSV_PATH, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_question = dict(row)
            if one_question_id is not None and one_question_id == user_question['id']:
                return user_question
            user_questions.append(user_question)
    return user_questions


def get_all_questions():
    all_questions = get_csv_question_data()
    return all_questions


def generate_id():
    pass















