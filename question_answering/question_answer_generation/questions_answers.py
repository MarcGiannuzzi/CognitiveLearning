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
    nlp_obj = None
    if(lang == "english"):
        nlp_obj = qg_pipeline_en
    elif(lang == "french"):
        nlp_obj = qg_pipeline_fr
    return nlp_obj


def cut_text(text):
    """
        Description : Fonction permettant de découper un texte en plusieurs inputs rentrés par la suite dans les modèles de génération de questions/réponses.
        Arguments : 
            - text : Texte dont on veut qu'il soit découpé.
        Returns : Une liste des différentes parties du texte entré en input.
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


def get_question_answers(text, qg_pipeline):
    """
        Description : Fonction permettant de récupérer les questions/réponses à partir d'un texte.
        Arguments : 
            - text : Texte dont on veut soutirer les questions/réponses.
        Returns : Une liste de questions/réponses générées.
    """
    all_questions_answers = []
    all_questions = []
    texts = cut_text(text)
    for text in texts:
        questions_answers = qg_pipeline(text)
        for question_answer in questions_answers:
            if question_answer['question'] not in all_questions:
                all_questions_answers.append(question_answer)
                all_questions.append(question_answer['question'])
    return all_questions_answers


if __name__ == "__main__":
    text_fr = """L'équipe de France de football, créée en 1904, 
    est l'équipe nationale qui représente la France dans les compétitions 
    internationales masculines de football, sous l'égide de la Fédération 
    française de football (FFF). Elle consiste à sélectionner les meilleurs 
    joueurs français. Ces derniers, composant cette équipe, sont traditionnellement 
    appelés Les Tricolores ou encore Les Bleus. De nos jours, c'est cette dernière 
    appellation qui est la plus usitée."""

    text_en = """Cognitive science is the interdisciplinary, scientific study of the mind and its processes. It examines the nature, the tasks, and the functions of cognition (in a broad sense). Cognitive scientists study intelligence and behavior, with a focus on how nervous systems represent, process, and transform information. Mental faculties of concern to cognitive scientists include language, perception, memory, attention, reasoning, and emotion; to understand these faculties, cognitive scientists borrow from fields such as linguistics, psychology, artificial intelligence, philosophy, neuroscience, and anthropology. The typical analysis of cognitive science spans many levels of organization, from learning and decision to logic and planning; from neural circuitry to modular brain organization. One of the fundamental concepts of cognitive science is that thinking can best be understood in terms of representational structures in the mind and computational procedures that operate on those structures.The goal of cognitive science is to understand the principles of intelligence with the hope that this will lead to better comprehension of the mind and of learning and to develop intelligent devices. The cognitive sciences began as an intellectual movement in the 1950s often referred to as the cognitive revolution."""

    questions_answers = qg_pipeline(text_fr)
    print(questions_answers)
