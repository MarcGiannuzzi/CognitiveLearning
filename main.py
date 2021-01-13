#test de push baptiste

from question_answer_generation.pipelines import pipeline

if __name__ == "__main__":
    qg_pipeline = pipeline(lang="french", task="question-generation")
    text = """L'équipe de France de football, créée en 1904, 
    est l'équipe nationale qui représente la France dans les compétitions 
    internationales masculines de football, sous l'égide de la Fédération 
    française de football (FFF). Elle consiste à sélectionner les meilleurs 
    joueurs français. Ces derniers, composant cette équipe, sont traditionnellement 
    appelés Les Tricolores ou encore Les Bleus. De nos jours, c'est cette dernière 
    appellation qui est la plus usitée."""
    
    questions_answers = qg_pipeline(text)
    print(questions_answers)
    #[{'answer': '1904', 'question': 'When was the team de France de football created?'}, 
    # {'answer': 'Les Tricolores ou encore Les Bleus', 'question': 'What are the last names of the team that represents the France in the competitions internationals masculines de football?'}, 
    # {'answer': 'la plus usitée', 'question': 'What is the name of the last appellation of France de football?'}]