from .pipelines import pipeline
from nltk import sent_tokenize


MAX_SIZE_INPUT = 511


def cut_text(text):
    """
        Description : Fonction permettant de découper un texte en plusieurs inputs rentrés par la suite dans les modèles de génération de questions/réponses.
        Arguments : 
            - text : Texte dont on veut qu'il soit découpé.
    """
    tokenized_sentence = sent_tokenize(text)
    counter = 0
    all_inputs = []
    one_input = ""
    for sentence in tokenized_sentence:
        sentence_size = len(sentence)
        if sentence_size > MAX_SIZE_INPUT:
            if one_input != "":
                all_inputs.append(one_input)
                counter = 0
                one_input = ""
            sentence = sentence[:MAX_SIZE_INPUT]
            all_inputs.append(sentence)
        else:
            if counter + sentence_size < MAX_SIZE_INPUT:
                counter += sentence_size
                one_input += sentence
            else:
                all_inputs.append(one_input)
                one_input = sentence
                counter = sentence_size
    if one_input != "":
        all_inputs.append(one_input)
    return all_inputs


def get_question_answers(text, lang, task="question-generation"):
    """
        Description : Fonction permettant de récupérer les questions/réponses à partir d'un texte.
        Arguments : 
            - text : Texte dont on veut soutirer les questions/réponses.
    """
    all_questions_answers = []
    texts = cut_text(text)
    qg_pipeline = pipeline(lang=lang, task=task)
    for text in texts:
        questions_answers = qg_pipeline(text)
        all_questions_answers += questions_answers
    return all_questions_answers
