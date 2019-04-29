import string
import random
import connection

QUESTION_CSV_PATH = connection.QUESTION_CSV_PATH
ANSWER_CSV_PATH = connection.ANSWER_CSV_PATH
QUESTION_HEADER = connection.QUESTION_HEADER
ANSWER_HEADER = connection.ANSWER_HEADER


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC;
    """)
    all_questions = cursor.fetchall()
    return all_questions


@connection.connection_handler
def get_question_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
    """, {'question_id': question_id})
    filtered_answers = cursor.fetchall()
    return filtered_answers


@connection.connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer
                    ORDER BY submission_time DESC;
    """)
    all_answers = cursor.fetchall()
    return all_answers


def convert_linebreak_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))


@connection.connection_handler
def get_all_answers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s
                    ORDER BY submission_time DESC;
    """, {'question_id': question_id})
    filtered_answers = cursor.fetchall()
    return filtered_answers


def generate_id(length=4):
    rand_letters = random.sample(string.ascii_lowercase, length)
    id_ = "".join(rand_letters)
    return id_


@connection.connection_handler
def send_user_input(existing_data, path, header):
    connection.write_csv_data(path, header, existing_data)
