import pandas as pd
import spacy
from spacy import displacy
import gensim
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import os
import json

NLP_EN = spacy.load('en_core_web_sm')

glove_file = './data/glove.6B.300d.txt'
tmp_file_en = './data/word2vec-glove.6B.300d.txt'
if not os.path.exists(tmp_file_en):
    glove2word2vec(glove_file, tmp_file_en)


ENGLISH_MODEL = KeyedVectors.load_word2vec_format(tmp_file_en)


def getNEStartIndices(doc):
    """
        Description : Fonction retournant l'index de chaque entités dans le texte
        Arguments : 
            - doc : texte de la reponse, auquel on a appliqué la fonction NLP_EN afin d'utiliser des fonctionnalités SPACY.
        Returns : Dictionnaire contenant toutes les entités du text.
    """
    try:
        neStarts = {}
        for ne in doc.ents:
            neStarts[ne.start] = ne

        return neStarts
    except:
        print("Error in getNEStartIndices")


def addWordsForParagraph(newWords, text):
    """
        Description : Fonction permettant de selectionner seulement les mots ou groupe de mots importants.
        Arguments : 
            - newWords : Liste vide.
            - text : La réponse à la question.
        Returns : Pas de retours. La fonction modifie la variable newWords en entrée.
    """
    try:
        doc = NLP_EN(text)

        neStarts = getNEStartIndices(doc)

        # index of word in spacy doc text
        i = 0

        while (i < len(doc)):
            # If the token is a start of a Named Entity, add it and push to index to end of the NE
            if (i in neStarts):
                word = neStarts[i]
                # add word

                newWords.append([word.text,
                                 word.label_,
                                 None,
                                 None,
                                 None])
                i = neStarts[i].end - 1
            # If not a NE, add the word if it's not a stopword or a non-alpha (not regular letters)
            else:
                if (doc[i].is_stop == False and doc[i].is_alpha == True):
                    word = doc[i]

                    wordLen = 1

                    newWords.append([word.text,
                                     None,
                                     word.pos_,
                                     word.tag_,
                                     word.dep_])
            i += 1
    except:
        print("Error in addWordsForParagraph")


def generateDf(text):
    """
        Description : Fonction créant un dataframe contenant les mots importants de la réponse.
        Arguments : 
            - text : La réponse à la question.
        Returns : Dataframe.
    """
    try:
        words = []
        addWordsForParagraph(words, text)

        wordColums = ['text', 'NER', 'POS', 'TAG', 'DEP']
        df = pd.DataFrame(words, columns=wordColums)

        return df
    except:
        print("Error in generateDf")


def blankAnswer(firstTokenIndex, lastTokenIndex, sentStart, sentEnd, doc):
    """
        Description : Fonction permettant de placer un BLANK au niveau d'un mot en particulier.
        Arguments : 
            - firstTokenIndex : index du 1er mot du groupe de mot à remplacer.
            - lastTokenIndex : index du dernier mot du groupe de mot à remplacer.
            - sentStart : Début de la phrase.
            - sentEnd : Fin de la phrase.
            - doc : texte de la reponse, auquel on a appliqué la fonction NLP_EN afin d'utiliser des fonctionnalités SPACY.            
        Returns : Phrase d'entrée avec un BLANK au niveau du toekn à remplacer.
    """
    try:
        leftPartStart = doc[sentStart].idx
        leftPartEnd = doc[firstTokenIndex].idx
        rightPartStart = doc[lastTokenIndex].idx + len(doc[lastTokenIndex])
        rightPartEnd = doc[sentEnd - 1].idx + len(doc[sentEnd - 1])

        question = doc.text[leftPartStart:leftPartEnd] + \
            '___' + doc.text[rightPartStart:rightPartEnd]

        return question
    except:
        print("Error in blankAnswer")


def addQuestions(answers, text):
    """
        Description : Fonction remplacant les mots importants par un BLANK.
        Arguments : 
            - answers : dictionnaire contenant les mots à remplacer.
            - text : réponse correcte.
        Returns : Liste de dictionnaires comme suit : [{'question': '___ has won the world cup in 2018', 'answer': 'France'}]
    """
    try:
        doc = NLP_EN(text)
        currAnswerIndex = 0
        qaPair = []

        # Check wheter each token is the next answer
        for sent in doc.sents:
            for token in sent:

                # If all the answers have been found, stop looking
                if currAnswerIndex >= len(answers):
                    break

                # In the case where the answer is consisted of more than one token, check the following tokens as well.
                answerDoc = NLP_EN(answers[currAnswerIndex]['word'])
                answerIsFound = True

                for j in range(len(answerDoc)):
                    if token.i + j >= len(doc) or doc[token.i + j].text != answerDoc[j].text:
                        answerIsFound = False

                # If the current token is corresponding with the answer, add it
                if answerIsFound:
                    question = blankAnswer(
                        token.i, token.i + len(answerDoc) - 1, sent.start, sent.end, doc)

                    qaPair.append(
                        {'question': question, 'answer': answers[currAnswerIndex]['word']})

                    currAnswerIndex += 1

        return qaPair
    except:
        print("Error in addQuestions")


def generate_distractors(answer, count):
    """
        Description : Fonction permettant de savoir si un string est une date ou non.
        Arguments : 
            - answer : String à checker pour savoir si ce dernier correspond à une date.
            - count : Ignore les tokens non connus ou non.
        Returns : Liste de mots similaires à celui en entrée.
    """
    try:
        answer = str.lower(answer)

        # Extracting closest words for the answer.
        try:
            closestWords = ENGLISH_MODEL.most_similar(
                positive=[answer], topn=count)
        except:
            # In case the word is not in the vocabulary, or other problem not loading embeddings
            return []

        # Return count many distractors
        distractors = list(map(lambda x: x[0], closestWords))[0:count]

        return distractors
    except:
        print("Error in generate_distractors")


def addDistractors(qaPairs, count):
    """
        Description : Fonction permettant de savoir si un string est une date ou non.
        Arguments : 
            - qaPairs : liste de dictionnaire ayant comme format : {'question': 'France has won the world cup in ___', 'answer': '2018'}
            - count : nombre de mots similaires à générer.
        Returns : dictionnaire comme suit : {'question': 'France has won the world cup in ___', 'answer': '2018', 'distractors': ['2022', '2016', '2014', '2019']}
    """
    try:
        for qaPair in qaPairs:
            distractors = generate_distractors(qaPair['answer'], count)
            qaPair['distractors'] = distractors

        return qaPairs
    except:
        print("Error in addDistractors")


def selectWords(df):
    """
        Description : Retourne la liste des mots à remplacer.
        Arguments : 
            - df : dataframe.
        Returns : Liste de mots à remplacer.
    """
    try:
        labeledAnswers = []
        for i in range(df.shape[0]):
            labeledAnswers.append({'word': df.iloc[i]['text']})

        return labeledAnswers
    except:
        print("Error in selectWords")


def generate_answers_en(text, number_possible_answers=4):
    """
        Description : Fonction principale.
        Arguments : 
            - text : La réponse à la question.
            - number_possible_answers : Nombre de fausses réponses générées.
        Returns : JSON contenant la réponse correcte ainsi qu'une liste avec les réponses alternatives.
    """
    try:
        test = json.dumps({'correct_answer': text,
                           'incorrect_answers': []
                           })

        test_json = json.loads(test)

        df = generateDf(text)
        if df.empty:
            print('DataFrame is empty!')

        else:
            labeledAnswers = selectWords(df)
            qaPairs = addQuestions(labeledAnswers, text)

            # all words selected will be replaced
            questions = addDistractors(
                qaPairs[:len(df)], number_possible_answers)

            counter = 0
            incorrect_answers = test_json["incorrect_answers"]
            for question in questions:
                for question_distractor in question['distractors']:
                    if counter < number_possible_answers:
                        incorrect_answer = question['question'].replace(
                            '___', question_distractor)

                        incorrect_answers.append((incorrect_answer))
                        counter += 1

        json_final = json.dumps(test_json)

        return json_final
    except:
        print("Error in generate_answers_en")
