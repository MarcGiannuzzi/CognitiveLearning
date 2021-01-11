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
            - sentence : Phrase à cleaner.
    """
    regex = re.compile('.\'|([^\s\w]|_|\n)')
    sentence = regex.sub('', sentence)
    sentence = sentence.lower()
    sentence = sentence.split(" ")

    for word in sentence:
        if word in STOP_WORDS:
            sentence.remove(word)

    sentence = " ".join(sentence)

    return sentence


def levenshtein_ratio_and_distance(s, t, ratio_calc=False):
    """
        Description : Calcule la distance de Levenshtein entre deux strings.
        Arguments : 
            - s : Premier string.
            - t : Second string.
            - ratio_calc : Si ratio_calc = True, la fonction calcule la distance ratio de similarité entre les deux strings.
            Pour tous i et j, distance[i,j] contiendra la distance Levenshtein entre les premiers i caractères de s et les  j premiers caractères de t.
    """
    # Initialize matrix of zeros
    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows, cols), dtype=int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
                cost = 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row - 1][col] + 1,  # Cost of deletions
                                     distance[row][col - 1] + \
                                     1,  # Cost of insertions
                                     distance[row - 1][col - 1] + cost)  # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "The strings are {} edits away".format(distance[row][col])


def limit_spelling(ratio):
    """
        Description : Vérifie si le ratio ne dépasse pas la limite acceptable.
        Arguments : 
            - ratio : Ratio à comparer à MIN_LEVENSHTEIN_RATIO.
    """
    if ratio < MIN_LEVENSHTEIN_RATIO:
        return False
    else:
        return True


def are_equivalent(right_a, supposed_a):
    """
        Description : Permet de savoir si deux strings sont considérés comme équivalents.
        Arguments : 
            - right_a : Vraie réponse.
            - supposed_a : Réponse de l'utilisateur.
    """
    levenshtein_ratio = levenshtein_ratio_and_distance(
        right_a, supposed_a, ratio_calc=True)
    a = limit_spelling(levenshtein_ratio)
    print("Levenshtein Ratio", levenshtein_ratio)
    return a


if __name__ == "__main__":
    supposed_answer = 'Nous mangeonsss chez Chirac'
    clean_supposed_answer = clean_sentence(supposed_answer)
    print("Cleaned answer : ", clean_supposed_answer)
    right_answer = "Je mange chez chirac"
    strings_are_equivalent = are_equivalent(
        right_answer, clean_supposed_answer)
    print(strings_are_equivalent)
