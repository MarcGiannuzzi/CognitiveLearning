import pandas as pd
import spacy
from spacy import displacy


import gensim
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import os

NLP_EN = spacy.load('en_core_web_sm')


def getNEStartIndexs(doc):
    neStarts = {}
    for ne in doc.ents:
        neStarts[ne.start] = ne

    return neStarts


def addWordsForParagrapgh(newWords, text):
    doc = NLP_EN(text)

    neStarts = getNEStartIndexs(doc)

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


def generateDf(text):
    words = []
    addWordsForParagrapgh(words, text)

    print("o")
    print(words)

    wordColums = ['text', 'NER', 'POS', 'TAG', 'DEP']
    df = pd.DataFrame(words, columns=wordColums)

    return df


def blankAnswer(firstTokenIndex, lastTokenIndex, sentStart, sentEnd, doc):
    leftPartStart = doc[sentStart].idx
    leftPartEnd = doc[firstTokenIndex].idx
    rightPartStart = doc[lastTokenIndex].idx + len(doc[lastTokenIndex])
    rightPartEnd = doc[sentEnd - 1].idx + len(doc[sentEnd - 1])

    question = doc.text[leftPartStart:leftPartEnd] + \
        '_____' + doc.text[rightPartStart:rightPartEnd]

    return question


def addQuestions(answers, text):
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


def generate_distractors(answer, count):
    answer = str.lower(answer)

    # Extracting closest words for the answer.
    try:
        closestWords = model.most_similar(positive=[answer], topn=count)
    except:
        # In case the word is not in the vocabulary, or other problem not loading embeddings
        return []

    # Return count many distractors
    distractors = list(map(lambda x: x[0], closestWords))[0:count]

    return distractors


def addDistractors(qaPairs, count):
    for qaPair in qaPairs:
        distractors = generate_distractors(qaPair['answer'], count)
        qaPair['distractors'] = distractors

    return qaPairs


def selectWords(df):

    labeledAnswers = []
    for i in range(df.shape[0]):
        labeledAnswers.append({'word': df.iloc[i]['text']})

    return labeledAnswers


def generate_answers(text):
    incorrect_answers = []
    original_answer = text
    df = generateDf(text)
    if df.empty:
        print('DataFrame is empty!')

    else:
        labeledAnswers = selectWords(df)
        qaPairs = addQuestions(labeledAnswers, text)

        # number 2 -> only the first 2 words selected will be replaced
        questions = addDistractors(qaPairs[:len(df)], 4)
        # number 4 -> 4 similar words will be searched

        for question in questions:
            if question['distractors'] != []:
                incorrect1 = question['question'].replace(
                    '_____', question['distractors'][1])
                incorrect2 = question['question'].replace(
                    '_____', question['distractors'][2])
                incorrect_answers.append(incorrect1)
                incorrect_answers.append(incorrect2)
            else:
                print("not in vocabulary")

    return incorrect_answers


if __name__ == "__main__":
    text = "France has won the world cup in 2018"
    incorrect_answers = generate_answers(text)
    print("incorrect_answers : ", incorrect_answers)
    # print("blanked_answers : ", blanked_answers)
