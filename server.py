from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list():
    user_questions = data_manager.get_all_questions(convert_linebreak=True)
    return render_template("list.html", user_questions=user_questions)


@app.route("/question/<question_id>")
def question(question_id):
    return render_template("question.html")


@app.route("/add-question")
def add_question():
    return render_template("add-question.html")


@app.route("/question/<question_id>/new-answer")
def answer(question_id):
    return render_template("add-answer.html")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
