# En invite de commandes, rentrer :
# set FLASK_APP=api_question_answering.py
# set FLASK_ENV=development
# Puis lancer le serveur :
# python -m flask run


from flask import Flask, jsonify, request
import json

# ------------ Utilitaires ------------
from question_answering.utils import *
# ------------ Réponses à trou ------------
from question_answering.incorrect_answers_generation.incorrect_answers import *
# ------------ Vérification d'une réponse ------------
from question_answering.correctness_answers.spelling import *
# ------------ Génération de questions réponses ------------
from question_answering.question_answer_generation.questions_answers import *

app = Flask(__name__)


@app.route('/question_answering/get_questions_answers', methods=['POST'])
def api_get_questions_answers():
    print("Question Answering Endpoint")
    data = request.get_json(force=True)
    text = data['text']
    print("Data received")
    text_language = detect_language(text)
    print("Language detected")
    qg_pipeline = get_nlp_object(text_language)
    questions_answers = get_question_answers(text, qg_pipeline)
    print("Questions answers made")
    result = jsonify(questions_answers=questions_answers)
    return result


@app.route('/question_answering/is_answer_correct', methods=['POST'])
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


@app.route('/question_answering/create_incorrect_answers', methods=['POST'])
def api_create_blank():
    print("Modify Answer Endpoint")
    data = request.get_json(force=True)
    text = data['text']
    print("Data received")
    detected_language = detect_language(text)
    all_answers = generate_answers(text, detected_language)
    print("All answers made")
    return all_answers


if __name__ == '__main__':
    print("API server starting.")
    app.run(debug=True)
