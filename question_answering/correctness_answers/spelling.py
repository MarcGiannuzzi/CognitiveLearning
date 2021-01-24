import numpy as np
import re
import nltk


STOP_WORDS = nltk.corpus.stopwords.words(
    'english') + nltk.corpus.stopwords.words('french')
MIN_LEVENSHTEIN_RATIO = 0.7


def clean_sentence(sentence):
    """
        Description : Clean la phrase pour être par la suite processable.
        Arguments : 
            - sentence : Phrase à nettoyer.
        Returns : Phrase nettoyée.
    """
    try:
        regex = re.compile('.\'|([^\s\w]|_|\n)')
        sentence = regex.sub('', sentence)
        sentence = sentence.lower()
        sentence = sentence.split(" ")

        for word in sentence:
            if word in STOP_WORDS:
                sentence.remove(word)

        sentence = " ".join(sentence)
        sentence = remove_accents(sentence)
        return sentence
    except:
        print("Error in clean_sentence")


def remove_accents(input_str):
    try:
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    except:
        print("Error in remove_accents")


def levenshtein_ratio_and_distance(s, t, ratio_calc=False):
    """
        Description : Calcule la distance de Levenshtein entre deux strings.
        Arguments : 
            - s : Premier string.
            - t : Second string.
            - ratio_calc : Si ratio_calc = True, la fonction calcule la distance ratio de similarité entre les deux strings.
            Pour tous i et j, distance[i,j] contiendra la distance Levenshtein entre les premiers i caractères de s et les  j premiers caractères de t.
        Returns : Le ratio s'il a a pu être calculé, un string sinon.
    """
    try:
        rows = len(s) + 1
        cols = len(t) + 1
        distance = np.zeros((rows, cols), dtype=int)

        for i in range(1, rows):
            for k in range(1, cols):
                distance[i][0] = i
                distance[0][k] = k

        for col in range(1, cols):
            for row in range(1, rows):
                if s[row - 1] == t[col - 1]:
                    cost = 0
                else:
                    if ratio_calc == True:
                        cost = 2
                    else:
                        cost = 1
                distance[row][col] = min(distance[row - 1][col] + 1,
                                         distance[row][col - 1] +
                                         1,
                                         distance[row - 1][col - 1] + cost)
        if ratio_calc == True:
            Ratio = ((len(s) + len(t)) -
                     distance[row][col]) / (len(s) + len(t))
            return Ratio
        else:
            return "The strings are {} edits away".format(distance[row][col])
    except:
        print("Error in levenshtein_ratio_and_distance")


def are_equivalent(right_a, supposed_a):
    """
        Description : Permet de savoir si deux strings sont considérés comme équivalents.
        Arguments : 
            - right_a : Vraie réponse.
            - supposed_a : Réponse de l'utilisateur.
        Returns : True si les réponses sont syntaxiquement équivalentes, False sinon.
    """
    try:
        levenshtein_ratio = levenshtein_ratio_and_distance(
            right_a, supposed_a, ratio_calc=True)
        if levenshtein_ratio < MIN_LEVENSHTEIN_RATIO:
            return False
        else:
            return True
    except:
        print("Error in are_equivalent")


if __name__ == "__main__":
    supposed_answer = 'Nous mangeonsss chez Chirac'
    clean_supposed_answer = clean_sentence(supposed_answer)
    clean_right_answer = clean_sentence(right_answer)
    print("Cleaned answer : ", clean_supposed_answer)
    right_answer = "Je mange chez chirac"
    strings_are_equivalent = are_equivalent(
        clean_right_answer, clean_supposed_answer)
    print(strings_are_equivalent)
