from .pipelines import pipeline
from nltk import sent_tokenize


MAX_SIZE_INPUT = 511

qg_pipeline_en = pipeline(lang="english", task="question-generation")
qg_pipeline_fr = pipeline(lang="french", task="question-generation")


def get_nlp_object(lang):
    """
        Description : Fonction permettant de retourner l'objet nlp qa-qg spécifique à la langue.
        Arguments : 
            - lang : Langue dont on veut obtenir l'objet nlp de qa-qg.
        Returns : L'objet permettant de générer les questions réponses.
    """
    try:
        nlp_obj = None
        if(lang == "english"):
            nlp_obj = qg_pipeline_en
        elif(lang == "french"):
            nlp_obj = qg_pipeline_fr
        return nlp_obj
    except:
        print("Error in get_nlp_object")


def get_question_answers(text, qg_pipeline):
    """
        Description : Fonction permettant de récupérer les questions/réponses à partir d'un texte.
        Arguments : 
            - text : Texte dont on veut soutirer les questions/réponses.
        Returns : Une liste de questions/réponses générées.
    """
    try:
        all_questions_answers = []
        all_questions = []
        questions_answers = qg_pipeline(text)
        for question_answer in questions_answers:
            if question_answer['question'] not in all_questions:
                all_questions_answers.append(question_answer)
                all_questions.append(question_answer['question'])
        return all_questions_answers
    except:
        print("Error in get_question_answers")
