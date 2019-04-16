from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection
import time

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list():
    user_questions = data_manager.get_all_questions(convert_linebreak=True)
    return render_template("list.html", user_questions=user_questions)


@app.route("/question/<question_id>")
def question_page(question_id):
    question = connection.get_csv_question_data(connection.QUESTION_CSV_PATH, question_id)
    answers = data_manager.get_all_answers_by_question_id(question_id)
    return render_template("question.html", question=question, answers=answers)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template('question.html')
    elif request.method == "POST":
    question = connection.get_csv_question_data(request)

        return redirect(url_for('route_list'))
    return render_template("add-question.html")


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def answer(question_id):
    if request.method == 'POST':
        id = data_manager.generate_id()
        submission_time = int(time.time())
        vote_number = 666
        question_id = question_id
        message = request.form['message']
        image = request.form['image']
        new_answer = {"id": id, "submission_time": submission_time, "vote_number": vote_number,
                      "question_id": question_id, "message": message, "image": image}
        existing_data = data_manager.get_all_answers()
        existing_data.insert(0, new_answer)
        connection.write_csv_data(connection.ANSWER_CSV_PATH, connection.ANSWER_HEADER, existing_data)
        return redirect(f'/question/{question_id}')
    elif request.method == 'GET':
        return render_template("add-answer.html", question_id=question_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
