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

# Creates a decorator to handle the database connection/cursor opening/closing.
# Creates the cursor with RealDictCursor, thus it returns real dictionaries, where the column names are the keys.
import os
import psycopg2
import psycopg2.extras


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper
