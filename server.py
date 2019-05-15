from flask import Flask, render_template, request, redirect, url_for, session
from psycopg2._psycopg import IntegrityError

import data_manager
from datetime import datetime

from util import hash_password, verify_password

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def five_latest_question():
    five_latest_questions = data_manager.get_five_latest_questions()
    return render_template("latest-questions.html", questions=five_latest_questions)


@app.route("/list")
def route_list():
    user_questions = data_manager.get_all_questions()
    return render_template("list.html", user_questions=user_questions)


@app.route("/list/order by:<order_by>/direction:<order_direction>")
def order_list_by(order_by, order_direction):
    user_questions = data_manager.get_all_questions(order_by=order_by, direction=order_direction)
    return render_template("ordered-list.html", user_questions=user_questions, order_by=order_by,
                           order_direction=order_direction)


@app.route("/question/<int:question_id>")  # done
def question_page(question_id):
    question = data_manager.get_question_by_question_id(question_id)
    answers = data_manager.get_all_answers_by_question_id(question_id)
    tags = data_manager.get_tags(question_id)
    question_comments = data_manager.get_question_comments(question_id)
    data_manager.question_view_number(question_id)
    return render_template("question.html", question=question, answers=answers, question_comments=question_comments,
                           tags=tags)


@app.route("/add-question", methods=["GET", "POST"])  # done
def add_question():
    if request.method == "GET":
        return render_template('add-question.html')
    elif request.method == "POST":
        submission_time = datetime.now().isoformat(timespec='seconds')
        view_number = 0
        vote_number = 0
        title = request.form['title'].capitalize()
        message = request.form['message'].capitalize()
        image = request.form['image']
        user_id = session['id']
        data_manager.post_new_question(submission_time, view_number, vote_number, title, message, image, user_id)
        return redirect(url_for('five_latest_question'))


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])  # done
def add_answer(question_id):
    question = data_manager.get_question_by_question_id(question_id)
    if request.method == 'POST':
        submission_time = datetime.now().isoformat(timespec='seconds')
        vote_number = 0
        question_id = question_id
        message = request.form['message']
        image = request.form['image']
        user_id = session['id']
        data_manager.add_new_answer(submission_time, vote_number, question_id, message, image, user_id)
        return redirect(url_for('question_page', question=question, question_id=question_id))
    elif request.method == 'GET':
        return render_template("add-answer.html", question=question, question_id=question_id)


@app.route("/answer/<answer_id>/vote-<modifier>")  # done
def answer_vote(answer_id, modifier):
    question_id = request.args.get('question_id')
    if modifier == "up":
        data_manager.vote_up_for_answer(answer_id)
    elif modifier == "down":
        data_manager.vote_down_for_answer(answer_id)
    return redirect(url_for('question_page', question_id=question_id))


@app.route("/question/<question_id>/vote-<modifier>")  # done
def question_vote(question_id, modifier):
    if modifier == "up":
        data_manager.vote_up_for_question(question_id)
    elif modifier == "down":
        data_manager.vote_down_for_question(question_id)
    return redirect(url_for('question_page', question_id=question_id))


@app.route("/question/<answer_id>/delete_answer")  # done
def delete_answer(answer_id):
    question_id = request.args.get('question_id')
    data_manager.delete_answer(answer_id)
    return redirect(url_for('question_page', question_id=question_id))


@app.route("/question/<question_id>/delete_question")  # done
def delete_question(question_id):
    data_manager.delete_question(question_id)  # original
    return redirect('/')


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])  # done
def edit_question(question_id):
    question = data_manager.get_question_by_question_id(question_id)
    question_id = question['id']
    if request.method == 'GET':
        return render_template('edit.html', question=question, question_id=question_id)
    elif request.method == 'POST':
        submission_time = datetime.now().isoformat(timespec='seconds')
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        data_manager.update_question(submission_time, title, message, image, question_id)
        return redirect(f'/question/{question_id}')


@app.route("/result", methods=['POST'])
def get_search_result():
    if request.method == 'POST':
        phrase = request.form['search']
        results = data_manager.get_search_result(phrase)
        return render_template("result.html", results=results)


@app.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def add_tag_to_question(question_id):
    tags = data_manager.get_existing_tags()
    if request.method == 'GET':
        error = False
        return render_template("add-tag.html", question_id=question_id, tags=tags, error=error)
    elif request.method == 'POST':
        return_record = request.form.to_dict()
        if 'newtag' in return_record:
            try:
                newtag = request.form.to_dict()['newtag']
                for tag in tags:
                    if newtag == tag['name']:
                        tag_id = data_manager.pass_tag_id(newtag)[0]['id']
                        data_manager.add_new_tag_to_question_tag(question_id, tag_id)
                        return redirect(f'/question/{question_id}')
                data_manager.add_new_tag_to_tags(newtag)
                tag_id = data_manager.pass_tag_id(newtag)[0]['id']
                data_manager.add_new_tag_to_question_tag(question_id, tag_id)
                return redirect(f'/question/{question_id}')
            except IntegrityError:
                error = True
                return render_template('add-tag.html', question_id=question_id, tags=tags, error=error)
        elif 'newtag' not in return_record:
            try:
                existingtag = request.form['selecttag']
                tag_id = data_manager.pass_tag_id(existingtag)[0]['id']
                data_manager.add_new_tag_to_question_tag(question_id, tag_id)
                return redirect(f'/question/{question_id}')
            except IntegrityError:
                error = True
                return render_template('add-tag.html', question_id=question_id, tags=tags, error=error)


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(tag_id, question_id):
    data_manager.delete_tag(tag_id, question_id)
    return redirect(url_for('question_page', question_id=question_id))


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == "POST":
        answer_id = None
        message = request.form['message'].capitalize()
        submission_time = datetime.now().isoformat(timespec='seconds')
        edited_count = None
        user_id = session['id']
        data_manager.add_new_comment(question_id, answer_id, message, submission_time, edited_count, user_id)
        return redirect(url_for('question_page', question_id=question_id))
    elif request.method == "GET":
        return render_template('add-question-comment.html', question_id=question_id)


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    answer = data_manager.get_answer_by_answer_id(answer_id)
    if request.method == "POST":
        question_id = None
        message = request.form['message'].capitalize()
        submission_time = datetime.now().isoformat(timespec='seconds')
        edited_count = None
        user_id = session['id']
        data_manager.add_new_comment(question_id, answer_id, message, submission_time, edited_count, user_id)
        return redirect(url_for('question_page', question_id=answer['question_id']))
    elif request.method == "GET":
        return render_template('add-answer-comment.html', question_id=answer['question_id'], answer_id=answer_id,
                               answer=answer)


@app.route("/question/<question_id>/comments")
def question_comments(question_id):
    comments = data_manager.get_question_comments(question_id)
    if request.method == "GET":
        return render_template('question-comments.html', comments=comments)


@app.route("/answer/<answer_id>/comments")
def answer_comments(answer_id):
    comments = data_manager.get_answer_comments(answer_id)
    if request.method == "GET":
        return render_template('answer-comments.html', comments=comments)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        error = False
        return render_template('registration.html', error=error)
    elif request.method == "POST":
        username = request.form['username']
        registration_date = datetime.now().isoformat(timespec='seconds')
        password = hash_password(request.form['password'])
        try:
            data_manager.registration(username, password, registration_date)
            return redirect('/')
        except IntegrityError:
            error = True
            return render_template('registration.html', error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        error = False
        return render_template("login.html", error=error)
    elif request.method == "POST":
        username = request.form['username']
        hashed_password = data_manager.get_password_from_user_name(username)
        result = verify_password(request.form['password'], hashed_password[0]['password'])
        if result:
            session['username'] = request.form['username']
            session['id'] = data_manager.get_id_from_user_name(session['username'])
            return redirect(url_for('five_latest_question'))
        else:
            error = True
            return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('five_latest_question'))


@app.route("/tags")
def tags():
    questions = data_manager.get_questions_by_tags()
    return render_template('tags.html', questions=questions)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
