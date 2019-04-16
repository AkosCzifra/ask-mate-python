from flask import Flask, render_template, request, redirect, url_for
import data_manager

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


@app.route("/add-question")
def add_question():
    return render_template("add-question.html")


@app.route("/question/<question_id>/new-answer")
def answer(question_id):
    if request.method == 'POST':
        id = data_manager.generate_id()
        submission_time = time.time()
        vote_number = request.form['vote_number']
        question_id = request.form['question_id']
        message = request.form['message']
        image = request.form['image']
        # the function that does not exist yet but writes all the crap.
        return redirect('/question/<question_id>/')
    elif request.method == 'GET':
        return render_template("add-answer.html")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
