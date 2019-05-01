from flask import Flask, render_template, request, redirect, url_for
import data_manager
from datetime import datetime

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list():
    user_questions = data_manager.get_all_questions()
    return render_template("list.html", user_questions=user_questions)


@app.route("/list/order by:<order_by>/direction:<order_direction>")
def order_list_by(order_by, order_direction):
    user_questions = data_manager.get_all_questions(order_by=order_by, direction=order_direction)
    return render_template("ordered-list.html", user_questions=user_questions, order_by=order_by, order_direction=order_direction)


@app.route("/question/<int:question_id>")  # done
def question_page(question_id):
    question = data_manager.get_question_by_question_id(question_id)
    answers = data_manager.get_all_answers_by_question_id(question_id)
    data_manager.question_view_number(question_id)
    return render_template("question.html", question=question, answers=answers)


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
        data_manager.post_new_question(submission_time, view_number, vote_number, title, message, image)
        return redirect(url_for('route_list'))


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])  # done
def add_answer(question_id):
    question = data_manager.get_question_by_question_id(question_id)
    if request.method == 'POST':
        submission_time = datetime.now().isoformat(timespec='seconds')
        vote_number = 0
        question_id = question_id
        message = request.form['message']
        image = request.form['image']
        data_manager.add_new_answer(submission_time, vote_number, question_id, message, image)
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
    data_manager.delete_question(question_id)
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


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
