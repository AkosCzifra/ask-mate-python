from datetime import datetime
import data_manager


def unix_to_date(timestamp, timezone=7200):
    timestamp += timezone
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def cast_questions():
    questions = data_manager.get_all_questions()
    for rows in questions:
        rows["submission_time"] = int(rows["submission_time"])
        rows["view_number"] = int(rows["view_number"])
        rows["vote_number"] = int(rows["vote_number"])
        rows["title"] = rows["title"].capitalize()
    return questions
