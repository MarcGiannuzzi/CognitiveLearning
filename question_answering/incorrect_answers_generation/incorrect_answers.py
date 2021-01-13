from .incorrect_answers_fr import *
from .incorrect_answers_en import *


def generate_answers(full_answer, lang="english"):
    """
        Description : Fonction permettant de créer plusieurs réponses (fausses) similaires à partir d'une réponse.
        Arguments :
            - full_answer : Réponse dont on veut le QCM (fausse).
            - voc : Objet vocabulaire d'une langue.
            - number_possible_answers : Nombre de réponses (fausses) générées.
        Returns : (blank_answer, possible_answers)
            - true_answer : La vraie réponse.
            - possible_answers : Dictionnaire contenant LA bonne réponse et une liste de plusieurs autres réponses fausses.
    """
    if lang == "french":
        all_answers = generate_answers_fr(full_answer)
    elif lang == "english":
        all_answers = generate_answers_en(full_answer)
    return all_answers


if __name__ == "__main__":
    all_answers_test = generate_answers(
        "Bonjour ! La guerre est terminée !", "french")
    print(all_answers_test)
