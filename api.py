# set FLASK_APP=api.py
# set FLASK_ENV=development
# python -m flask run


from flask import Flask, jsonify, request
import json

from utils.preprocessing import *
from utils.spelling import *

from create_incorrect_answers import incorrect_answers_fr
from create_incorrect_answers import incorrect_answers_en

from question_answer_generation.questions_answers import get_question_answers


app = Flask(__name__)


@app.route('/api/get_questions_answers', methods=['POST'])
def api_get_questions_answers():
    print("Question Answering Endpoint")
    data = request.get_json(force=True)
    text = data['text']
    print("Data received")
    text_language = detect_language(text)
    print("Language detected")
    questions_answers = get_question_answers(text, text_language)
    print("Questions answers made")
    result = jsonify(questions_answers=questions_answers)
    return result


@app.route('/api/is_answer_correct', methods=['POST'])
def api_is_answer_correct():
    print("Is Answer Corrrect Endpoint")
    data = request.get_json(force=True)
    true_answer = data['true_answer']
    false_answer = data['false_answer']
    print("Data received")
    are_answers_equivalent = are_equivalent(true_answer, false_answer)
    print("Are answers equivalent made")
    result = jsonify(are_equivalent=are_answers_equivalent)
    return result


@app.route('/api/api_detect_language', methods=['POST'])
def api_detect_language():
    print("Spelling Corrrect Endpoint")
    data = request.get_json(force=True)
    text = data['text']
    print("Data received")
    detected_language = detect_language(text)
    print("Detect language made")
    result = jsonify(detected_language=detected_language)
    return result


@app.route('/api/api_modify_answer', methods=['POST'])
def api_modify_answer():
    print("Modify Answer Endpoint")
    data = request.get_json(force=True)
    answer = data['answer']
    print("Data received")
    detected_language = detect_language(answer)
    false_answer = None
    if detected_language == "french":
        false_answer = incorrect_answers_fr.modify_answer_to_incorrect(answer)
    else:
        false_answer = incorrect_answers_en.generate_answers(answer)
    print("False answer made")
    result = jsonify(answer_modified=false_answer)
    return result


@app.route('/api/api_create_blank', methods=['POST'])
def api_create_blank():
    print("Modify Answer Endpoint")
    data = request.get_json(force=True)
    text = data['text']
    print("Data received")
    detected_language = detect_language(text)
    blank_answers = None
    if detected_language == "french":
        blank_answers = incorrect_answers_fr.modify_answer_to_blank(text)
    # else:
    #     blank_answers = incorrect_answers_en.blankAnswer(answer)
    print("Blank answers made")
    result = jsonify(blank_answers=blank_answers)
    return result


if __name__ == '__main__':
    print("API server starting.")
    app.run(debug=True)
