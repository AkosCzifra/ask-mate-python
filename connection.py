import csv
import os

QUESTION_CSV = 'question.csv'
ANSWER_CSV = 'answer.csv'
QUESTION_CSV_PATH = os.getenv('QUESTION_CSV_PATH') if 'QUESTION_CSV_PATH' in os.environ else QUESTION_CSV
ANSWER_CSV_PATH = os.getenv('ANSWER_CSV_PATH') if 'ANSWER_CSV_PATH' in os.environ else ANSWER_CSV
QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADER = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_csv_question_data(data_table, one_question_id=None):
    user_questions = []
    with open(data_table, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_question = dict(row)
            if one_question_id is not None and one_question_id == user_question['id']:
                return user_question
            user_questions.append(user_question)
    return user_questions


def write_csv_data(data_table, header, existing_data):
    with open(data_table, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, quotechar='"', fieldnames=header)
        writer.writeheader()

        for row in existing_data:
            writer.writerow(row)
