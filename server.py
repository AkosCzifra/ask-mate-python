from flask import Flask, render_template, request, redirect, url_for
import data_manager
import time
import util
import connection

app = Flask(__name__)


@app.route("/")
@app.route("/list", methods=["GET", "POST"])
def route_list():
    user_questions = data_manager.get_all_questions(convert_linebreak=True)
    if request.method == "GET":
        user_questions.sort(key=lambda x: x["submission_time"], reverse=True)
        return render_template("list.html", user_questions=user_questions, util=util)
    if request.method == "POST":
        order_by = request.form['order_by']
        order_direction = request.form['order_direction']
        user_questions = util.cast_questions()
        if order_direction == 'asc':
            user_questions.sort(key=lambda x: x[order_by], reverse=False)
        else:
            user_questions.sort(key=lambda x: x[order_by], reverse=True)
        data_manager.send_user_input(user_questions, data_manager.QUESTION_CSV_PATH, data_manager.QUESTION_HEADER)
        return render_template("list.html", user_questions=user_questions, util=util)


@app.route("/list/<order_by>/<order_direction>")
def order_list(order_by, order_direction):
    user_questions = data_manager.get_all_questions(convert_linebreak=True)
    if order_direction == 'asc':
        user_questions.sort(key=lambda x: x[order_by], reverse=False)
    else:
        user_questions.sort(key=lambda x: x[order_by], reverse=True)
    data_manager.send_user_input(user_questions, data_manager.QUESTION_CSV_PATH, data_manager.QUESTION_HEADER)
    return redirect(url_for('route_list'))


@app.route("/question/<question_id>")
def question_page(question_id):
    question = data_manager.get_all_questions(key_id=question_id)
    answers = data_manager.get_all_answers_by_question_id(question_id)
    return render_template("question.html", question=question, answers=answers)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template('add-question.html')
    elif request.method == "POST":
        id = data_manager.generate_id()
        submission_time = int(time.time())
        view_number = 0
        vote_number = 0
        title = request.form['title'].capitalize()
        message = request.form['message'].capitalize()
        image = request.form['image']
        new_question = {"id": id, "submission_time": submission_time, "view_number": view_number,
                        "vote_number": vote_number, "title": title, "message": message, "image": image}
        existing_data = data_manager.get_all_questions()
        existing_data.insert(0, new_question)
        data_manager.send_user_input(existing_data, data_manager.QUESTION_CSV_PATH, data_manager.QUESTION_HEADER)
        return redirect(url_for('route_list'))


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def answer(question_id):
    question = data_manager.get_all_questions(key_id=question_id)
    if request.method == 'POST':
        id = data_manager.generate_id()
        submission_time = int(time.time())
        vote_number = 0
        question_id = question_id
        message = request.form['message']
        image = request.form['image']
        new_answer = {"id": id, "submission_time": submission_time, "vote_number": vote_number,
                      "question_id": question_id, "message": message, "image": image}
        existing_data = data_manager.get_all_answers()
        existing_data.insert(0, new_answer)
        data_manager.send_user_input(existing_data, data_manager.ANSWER_CSV_PATH, data_manager.ANSWER_HEADER)
        return redirect(f'/question/{question_id}')
    elif request.method == 'GET':
        return render_template("add-answer.html", question=question, question_id=question_id)


@app.route("/answer/<answer_id>/vote-<modifier>")
def answer_vote(answer_id, modifier):
    question_id = request.args.get('question_id')
    answers = data_manager.get_all_answers(True)
    for answer in answers:
        if answer['id'] == answer_id:
            if modifier == "up":
                answer['vote_number'] = int(answer.get('vote_number')) + 1
            elif modifier == "down":
                answer['vote_number'] = int(answer.get('vote_number')) - 1
            data_manager.send_user_input(answers, data_manager.ANSWER_CSV_PATH, data_manager.ANSWER_HEADER)
            return redirect(url_for('question_page', question_id=question_id))


@app.route("/question/<answer_id>/delete_answer")
def delete_answer(answer_id):
    question_id = request.args.get('question_id')
    answers = data_manager.get_all_answers(True)
    for i in range(len(answers)):
        if answers[i]['id'] == answer_id:
            del answers[i]
            data_manager.send_user_input(answers, data_manager.ANSWER_CSV_PATH, data_manager.ANSWER_HEADER)
            return redirect(url_for('question_page', question_id=question_id))
    return "Unexpected error: the answer was not found. Please go back to the home page!"


@app.route("/question/<question_id>/delete_question")
def delete_question(question_id):
    questions = data_manager.get_all_questions(True)
    for i in range(len(questions)):
        if questions[i]['id'] == question_id:
            del questions[i]
            data_manager.send_user_input(questions, data_manager.QUESTION_CSV_PATH, data_manager.QUESTION_HEADER)
            return redirect('/')
    return "Unexpected error 404: the answer was not found. Please go back to the home page!"


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    question_id = question_id
    questions = data_manager.get_all_questions(True)
    question = data_manager.get_all_questions(key_id=question_id)
    if request.method == 'GET':
        return render_template('edit.html', question=question, question_id=question_id)
    elif request.method == 'POST':
        submission_time = int(time.time())
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        for question in questions:
            if question['id'] == question_id:
                question['submission_time'] = submission_time
                question['title'] = title.capitalize()
                question['message'] = message.capitalize()
                question['image'] = image
                data_manager.send_user_input(questions, data_manager.QUESTION_CSV_PATH, data_manager.QUESTION_HEADER)
                return redirect(f'/question/{question_id}')
    return redirect('/')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
