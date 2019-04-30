import connection
from datetime import datetime


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
    return filtered_answers[0]


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                   DELETE FROM comment WHERE question_id = %(question_id)s;
                   DELETE FROM answer WHERE question_id = %(question_id)s;
                   DELETE FROM question WHERE id = %(question_id)s;
    """, {'id': question_id, 'question_id': question_id})


@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answer WHERE id=%(answer_id)s
    """, {'answer_id': answer_id})


@connection.connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer
                    ORDER BY submission_time DESC;
    """)
    all_answers = cursor.fetchall()
    return all_answers


@connection.connection_handler
def get_all_answers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s
                    ORDER BY submission_time DESC;
    """, {'question_id': question_id})
    filtered_answers = cursor.fetchall()
    return filtered_answers


@connection.connection_handler
def post_new_question(cursor, submission_time, view_number, vote_number, title, message, image):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s)
    """, {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number, 'title': title,
          'message': message, 'image': image})


@connection.connection_handler
def add_new_answer(cursor, submission_time, vote_number, question_id, message, image):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s)
    """, {'submission_time': submission_time, 'vote_number': vote_number, 'question_id': question_id,
          'message': message, 'image': image})


@connection.connection_handler
def update_question(cursor, submission_time, title, message, image, question_id):
    cursor.execute("""
                    UPDATE question
                    SET submission_time = %(submission_time)s, title = %(title)s, message = %(message)s, image = %(image)s
                    WHERE id=%(question_id)s
    """, {'submission_time': submission_time, 'title': title, 'message': message, 'image': image,
          'question_id': question_id})
