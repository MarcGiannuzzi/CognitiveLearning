from nltk import wordpunct_tokenize
import nltk
from nltk.corpus import stopwords
from nltk import sent_tokenize


def calc_languages_ratios(text):
    """
        Description : Fonction permettant de calculer les ratios (ratio élevé correspond à une grand chance que le texte entré soit de la langue correspondante).
        Arguments : 
            - text : Texte dont on veut les ratios pour chaque langue.
        Returns : Un dictionnaire contenant en clés les différentes langues et en valeurs les ratios correspondants. La langue ayant le plus gros ratio est celle du texte.
    """
    try:
        ratios = {}
        tokens = wordpunct_tokenize(text)
        words = [word.lower() for word in tokens]
        for lang in stopwords.fileids():
            stopwords_set = set(stopwords.words(lang))
            words_set = set(words)
            common_words = words_set.intersection(stopwords_set)
            ratios[lang] = len(common_words)
        return ratios
    except:
        print("Error in calc_languages_ratios")


def detect_language(text):
    """
        Description : Fonction permettant de détecter le langage du texte rentré en input.
        Arguments : 
            - text : Texte dont on veut la langue.
        Returns : Le langage detecté en string.
    """
    try:
        ratios = calc_languages_ratios(text)
        most_rated_language = max(ratios, key=ratios.get)
        return str(most_rated_language)
    except:
        print("Error in detect_language")
