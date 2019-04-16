from flask import Flask, render_template, request, redirect, url_for
import data_manager
import time
import util
import connection


app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list():
    user_questions = data_manager.get_all_questions(convert_linebreak=True)
    return render_template("list.html", user_questions=user_questions, util=util)


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
        title = request.form['title']
        message = request.form['message']
        new_question = {"id": id, "submission_time": submission_time, "view_number": view_number,
                        "vote_number": vote_number, "title": title, "message": message}
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


@app.route("/question/<question_id>/up-vote", methods=['POST'])
def up_vote(question_id,answer_id):
    answers = data_manager.get_all_answers_by_question_id(question_id)
    for answer in answers:
        if answer['answer_id'] == answer_id:
            answer['vote_number'] += 1
    return redirect("/question/<question_id>/")


@app.route("/question/<question_id>/down-vote", methods=['GET', 'POST'])
def down_vote(question_id, answer_id):
    answers = data_manager.get_all_answers_by_question_id(question_id)
    for answer in answers:
        if answer['answer_id'] == answer_id:
            answer['vote_number'] -= 1
            connection.write_csv_data(connection.ANSWER_CSV, connection.ANSWER_HEADER, answers)
            return redirect("/question/<question_id>/")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
