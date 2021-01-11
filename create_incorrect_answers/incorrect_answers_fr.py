import gensim
from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors
import fr_core_news_sm
from dateutil.parser import parse
import spacy
from spacy import displacy
from collections import Counter
import random
import nltk
import datetime
import os

NUMBER_POSSIBLE_ANSWERS = 3
AVOID_TAGS = ["ADV_", "ADP_", "VERB", "PRON", "DET_", "AUX_", "PUNC"]
NLP_FR = spacy.load('fr_core_news_sm')

glove_file = './data/glove.6B.300d.txt'
tmp_file = './data/word2vec-glove.6B.300d.txt'
if not os.path.exists(tmp_file):
    glove2word2vec(glove_file, tmp_file)

FRENCH_MODEL = KeyedVectors.load_word2vec_format(tmp_file)


def is_date(string, fuzzy=False):
    """
        Description : Fonction permettant de savoir si un string est une date ou non.
        Arguments : 
            - string : String à checker pour savoir si ce dernier correspond à une date.
            - fuzzy : Ignore les tokens non connus ou non.
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def modify_date(answer_date):
    """
        Description : Fonction permettant de modifier, au hasard, une date à partir d'une autre dans le but de créer une fausse date.
        Arguments : 
            - answer_date : Date dont on veut une version modifiée (fausse).
    """
    int_confidence = 3
    new_answer_year = answer_date.year + \
        random.randint(-int_confidence, int_confidence)
    new_answer_month = answer_date.month + random.randint(0, int_confidence)
    new_answer_day = answer_date.day + random.randint(0, int_confidence)
    return datetime.datetime(new_answer_year, new_answer_month, new_answer_day)


def modify_answer_to_blank(answer, voc=NLP_FR, number_possible_answers=3):
    """
        Description : Fonction permettant de créer plusieurs réponses (fausses) similaires à partir d'une réponse.
        Arguments : 
            - answer : Réponse dont on veut une version modifiée (fausse).
            - voc : Objet vocabulaire d'une langue.
            - number_possible_answers : Nombre de réponses (fausses) générées.
    """
    answer = answer.lower()
    possible_answers = []
    doc = voc(answer)
    important_words_answer = [X for X in doc if X.tag_[
        :4] not in AVOID_TAGS]  # 4 == taille des AVOID_TAGS
    important_word_answer = important_words_answer[random.randint(
        0, len(important_words_answer) - 1)]
    # Faire en sorte que le replace puisse targeter l'unique élément à prendre en compte, et non tous ou un/plusieurs mauvais.
    blank_answer = answer.replace(important_word_answer.text, "___")
    if is_date(important_word_answer.text):
        for _ in range(number_possible_answers):
            answer_date = parse(important_word_answer.text)
            new_date = modify_date(answer_date)
            possible_answers.append(new_date)
    else:
        for _ in range(number_possible_answers):
            similar_words = FRENCH_MODEL.most_similar(
                important_word_answer.text)
            random_position_answer = random.randint(
                0, int((len(similar_words) - 1) / 2))
            other_answer = similar_words[random_position_answer][0]
            possible_answers.append(other_answer)

    return blank_answer, possible_answers


def modify_answer_to_incorrect(answer, voc=NLP_FR, model=FRENCH_MODEL):
    """
        Description : Fonction permettant de modifier, au hasard, une réponse, dans le but d'en générer une nouvelle (fausse) similaire.
        Arguments : 
            - answer : Réponse dont on veut une version modifiée (fausse).
            - voc : Objet vocabulaire d'une langue.
            - model : Modèle permettant d'obtenir les mots similaires.
    """
    answer = answer.lower()
    doc = voc(answer)
    important_words_answer = [X for X in doc if X.tag_[
        :4] not in AVOID_TAGS]  # 4 == taille des AVOID_TAGS
    for important_word_answer in important_words_answer:
        try:
            if is_date(important_word_answer.text):
                answer_date = parse(important_word_answer.text)
                new_date = modify_date(answer_date)
                answer = answer.replace(
                    important_word_answer.text, str(new_date), 1)
            else:
                similar_words = FRENCH_MODEL.most_similar(
                    important_word_answer.text)
                random_position_answer = random.randint(
                    0, len(similar_words) - 1)
                other_answer = similar_words[random_position_answer][0]
                answer = answer.replace(
                    important_word_answer.text, other_answer)
        except KeyError:
            pass
    return answer


if __name__ == "__main__":
    answer = "Chez Chirac nous mangeons bien."
    answer = "La France a gagné la coupe du monde en 2018."
    answer_modified = modify_answer_to_incorrect(answer, NLP_FR, FRENCH_MODEL)
    answer_blanked = modify_answer_to_blank(
        answer, NLP_FR, NUMBER_POSSIBLE_ANSWERS)
    print("answer_modified : ", answer_modified)
    print("answer_blanked : ", answer_blanked)
