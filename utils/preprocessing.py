
from nltk import wordpunct_tokenize
import nltk
from nltk.corpus import stopwords
from nltk import sent_tokenize


def get_nlp_object(langue):
    """
        Description : Fonction permettant de retourner l'objet nlp qa-qg spécifique à la langue.
        Arguments : 
            - langue : Langue dont on veut obtenir l'objet nlp de qa-qg.
    """
    nlp_obj = None
    if(langue == "english"):
        nlp_obj = nlp_en
    if(langue == "french"):
        nlp_obj = nlp_fr
    return nlp_obj


def calc_languages_ratios(text):
    """
        Description : Fonction permettant de calculer les ratios (ratio élevé correspond à une grand chance que le texte entré soit de la langue correspondante).
        Arguments : 
            - text : Texte dont on veut les ratios pour chaque langue.
    """
    ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]
    for lang in stopwords.fileids():
        stopwords_set = set(stopwords.words(lang))
        words_set = set(words)
        common_words = words_set.intersection(stopwords_set)
        ratios[lang] = len(common_words)
    return ratios


def detect_language(text):
    """
        Description : Fonction permettant de détecter le langage du texte rentré en input.
        Arguments : 
            - text : Texte dont on veut la langue.
    """
    ratios = calc_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    return str(most_rated_language)


if __name__ == "__main__":
    text = """Chacun peut publier immédiatement du contenu en ligne, à condition de respecter les règles essentielles établies par la Fondation Wikimedia et par la communauté ; par exemple, la vérifiabilité du contenu, l'admissibilité des articles et garder une attitude cordiale.
            De nombreuses pages d’aide sont à votre disposition, notamment pour créer un article, modifier un article ou insérer une image. N’hésitez pas à poser une question pour être aidé dans vos premiers pas, notamment dans un des projets thématiques ou dans divers espaces de discussion.
            Les pages de discussion servent à centraliser les réflexions et les remarques permettant d’améliorer les articles."""
    print(len(cut_text(text)))
    print(detect_language(text))
