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

NUMBER_POSSIBLE_ANSWERS = 4
AVOID_TAGS = ["ADV_", "ADP_", "VERB", "PRON", "DET_",
              "AUX_", "PUNC"]  # Les éléments doivent être de taille 4
NLP_FR = spacy.load('fr_core_news_sm')

tmp_file_fr = "./data/frWac_no_postag_phrase_500_cbow_cut100.bin"
FRENCH_MODEL = KeyedVectors.load_word2vec_format(
    tmp_file_fr, binary=True, unicode_errors="ignore")


def is_date(string, fuzzy=False):
    """
        Description : Fonction permettant de savoir si un string est une date ou non.
        Arguments :
            - string : String à checker pour savoir si ce dernier correspond à une date.
            - fuzzy : Ignore les tokens non connus ou non.
        Returns : True si le string est une date, false sinon.
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
        Returns : La date modifiée (au hasard)

    """
    int_confidence = 3
    new_answer_year = answer_date.year + \
        random.randint(-int_confidence, int_confidence)
    new_answer_month = answer_date.month + random.randint(0, int_confidence)
    new_answer_day = answer_date.day + random.randint(0, int_confidence)
    return datetime.datetime(new_answer_year, new_answer_month, new_answer_day)


def generate_answers_fr(full_answer, number_possible_answers=4):
    """
        Description : Fonction permettant de créer plusieurs réponses (fausses) similaires à partir d'une réponse.
        Arguments :
            - full_answer : Réponse dont on veut le QCM (fausse).
            - voc : Objet vocabulaire d'une langue.
            - number_possible_answers : Nombre de réponses (fausses) générées.
        Returns : (blank_answer, possible_answers)
            - true_false_answers : Dictionnaire contenant LA bonne réponse et une liste de plusieurs autres réponses fausses.
    """
    full_answer = full_answer.lower()
    possible_answers = []
    doc = NLP_FR(full_answer)
    important_words_answer = [X for X in doc if X.tag_[
        :4] not in AVOID_TAGS]  # 4 == taille des AVOID_TAGS
    important_word_answer = important_words_answer[random.randint(
        0, len(important_words_answer) - 1)]
    # Faire en sorte que le replace puisse targeter l'unique élément à prendre en compte, et non tous ou un/plusieurs mauvais.
    true_answer = important_word_answer.text
    if is_date(true_answer):
        for _ in range(number_possible_answers):
            answer_date = parse(true_answer)
            new_date = modify_date(answer_date)
            possible_answer = full_answer.replace(answer_date, new_date, 1)
            possible_answers.append(possible_answer)
    else:
        random_indices = []
        for _ in range(number_possible_answers):
            similar_words = FRENCH_MODEL.most_similar(
                true_answer)
            random_position_answer = random.randint(
                0, int((len(similar_words) - 1) / 2))
            while random_position_answer in random_indices:
                random_position_answer = random.randint(
                    0, int((len(similar_words) - 1) / 2))
            random_indices.append(random_position_answer)
            other_answer = similar_words[random_position_answer][0]
            possible_answer = full_answer.replace(true_answer, other_answer, 1)
            possible_answers.append(possible_answer)

    true_false_answers = {"correct_answer": full_answer,
                          "incorrect_answers": possible_answers}
    return true_false_answers


if __name__ == "__main__":
    text = "J'irai manger chez vous demain soir."
    incorrect_answers = generate_answers_fr(text)
    print("incorrect_answers : ", incorrect_answers)
