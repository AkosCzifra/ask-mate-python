import connection


@connection.connection_handler
def get_all_questions(cursor, order_by="submission_time", direction="DESC"):
    if order_by == "submission_time" and direction == "DESC":
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY submission_time DESC;
                       """)
        all_questions = cursor.fetchall()
        return all_questions
    elif order_by == "submission_time" and direction == "ASC":
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY submission_time ASC;
                       """)
        all_questions = cursor.fetchall()
        return all_questions
    if order_by == "title" and direction == "DESC":
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY title DESC;
                       """)
        all_questions = cursor.fetchall()
        return all_questions
    elif order_by == "title" and direction == "ASC":
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY title ASC;
                       """)
        all_questions = cursor.fetchall()
        return all_questions
    if order_by == "view_number" and direction == "DESC":
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY view_number DESC;
                       """)
        all_questions = cursor.fetchall()
        return all_questions
    elif order_by == "view_number" and direction == "ASC":
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY view_number ASC;
                       """)
        all_questions = cursor.fetchall()
        return all_questions
    if order_by == "vote_number" and direction == "DESC":
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY vote_number DESC;
                       """)
        all_questions = cursor.fetchall()
        return all_questions
    elif order_by == "vote_number" and direction == "ASC":
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY vote_number ASC;
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
                    DELETE FROM question_tag WHERE question_id = %(question_id)s;
                    DELETE FROM comment WHERE question_id = %(question_id)s;
                    DELETE FROM answer WHERE question_id = %(question_id)s;
                    DELETE FROM question WHERE id = %(question_id)s;
    """, {'id': question_id, 'question_id': question_id})


@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment WHERE answer_id=%(answer_id)s;
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
def vote_up_for_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number+1
                    WHERE id=%(answer_id)s
    """, {'answer_id': answer_id})


@connection.connection_handler
def vote_down_for_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number-1
                    WHERE id=%(answer_id)s
    """, {'answer_id': answer_id})


@connection.connection_handler
def vote_down_for_question(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number-1
                    WHERE id=%(question_id)s
    """, {'question_id': question_id})


@connection.connection_handler
def vote_up_for_question(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number+1
                    WHERE id=%(question_id)s
    """, {'question_id': question_id})


@connection.connection_handler
def question_view_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number+1
                    WHERE id=%(question_id)s
    """, {'question_id': question_id})


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


@connection.connection_handler
def get_five_latest_questions(cursor):
    cursor.execute("""
                SELECT * FROM question
                ORDER BY submission_time DESC
                LIMIT 5;
    """)
    five_latest_question = cursor.fetchall()
    return five_latest_question


@connection.connection_handler
def get_search_result(cursor, phrase):
    phrase = f'%{phrase}%'
    cursor.execute("""
                    SELECT DISTINCT title,question.id FROM question
                    LEFT JOIN answer ON question.id = answer.question_id
                    WHERE title ILIKE %(phrase)s OR question.message ILIKE %(phrase)s OR answer.message ILIKE %(phrase)s   
    """, {'phrase': phrase})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def add_new_comment(cursor, question_id, answer_id, message, submission_time, edited_count):
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s,%(answer_id)s,%(message)s,%(submission_time)s,%(edited_count)s)
    """, {'question_id': question_id, 'answer_id': answer_id, 'message': message, 'submission_time': submission_time,
          'edited_count': edited_count})


@connection.connection_handler
def get_question_comments(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %(question_id)s
                    ORDER BY submission_time DESC;
    """, {'question_id': question_id})
    all_comments = cursor.fetchall()
    return all_comments


@connection.connection_handler
def get_answer_comments(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE answer_id = %(answer_id)s
                    ORDER BY submission_time DESC;
    """, {'answer_id': answer_id})
    all_comments = cursor.fetchall()
    return all_comments


@connection.connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(answer_id)s;
    """, {'answer_id': answer_id})
    answer = cursor.fetchall()
    return answer[0]


@connection.connection_handler
def add_new_tag_to_tags(cursor, name):
    cursor.execute("""
                    INSERT INTO tag (name)
                    VALUES (%(name)s);
    """, {'name': name})


@connection.connection_handler
def add_new_tag_to_question_tag(cursor, question_id, tag_id):
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id)
                    VALUES (%(question_id)s, %(tag_id)s)
    """, {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def get_tags(cursor, question_id):
    cursor.execute("""
                    SELECT name,question_id,tag_id
                    FROM ((question_tag
                    INNER JOIN tag ON tag_id = tag.id)
                    INNER JOIN question ON question_id = question.id)
                    WHERE question_id=%(question_id)s;             
    """, {'question_id': question_id})
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def pass_tag_id(cursor, name):
    cursor.execute("""
                    SELECT id
                    FROM tag
                    WHERE name = %(name)s
    """, {'name': name})
    id_ = cursor.fetchall()
    return id_


@connection.connection_handler
def delete_tag(cursor, tag_id, question_id):
    cursor.execute("""
                    DELETE FROM question_tag WHERE question_id=%(question_id)s AND tag_id=%(tag_id)s;               
    """, {'tag_id': tag_id, 'question_id': question_id})


@connection.connection_handler
def delete_answer_comment_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment WHERE answer_id=%(answer_id)s;
    """, {'answer_id': answer_id})


@connection.connection_handler
def get_existing_tags(cursor):
    cursor.execute("""
                    SELECT DISTINCT name FROM tag;
    """)
    tags = cursor.fetchall()
    return tags

@connection.connection_handler
def registration(cursor, username, password, registration_date):
    cursor.execute("""
                    INSERT INTO userdata (user_name, password, registration_date) 
                    VALUES (%(username)s, %(password)s, %(registration_date)s);
    """, {'username': username, 'password': password, 'registration_date': registration_date})


@connection.connection_handler
def get_password_from_user_name(cursor, username):
    cursor.execute("""
                    SELECT password FROM userdata
                    WHERE %(username)s = user_name
    """, {"username": username})
    password = cursor.fetchall()
    return password
