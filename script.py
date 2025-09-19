import random
import unidecode

base_AI = {
    'salutation' : {
        'mots' : ['bonjour', 'salut', 'coucou', 'bonsoir', 'hey', 'yo', 'Hello !'],
        'reponses' : ['Salut !', 'Coucou !', 'Bonjour !', 'Hey !', 'Hello !']
    },
    'etat' : {
        'mots' : ['comment ca va', 'ca va', 'comment vas tu', 'comment tu vas', 'ça va', 'tout va bien'],
        'reponses' : ['Ça va bien merci ! Et toi ?', 'Je vais bien, merci.', 'Tout roule !']
    },
    'identiter' : {
        'mots' : ['qui es tu', 'tu es qui', 'c’est quoi ton nom', 'qui es-tu'],
        'reponses' : ['Je suis ton mini AI.', 'Je suis une intelligence artificielle.', 'Une petite IA à ton service !'],
    },
    "meteo": {
        "mots": ['quel temps', 'météo', 'il fait beau', 'il pleut', 'temps qu’il fait'],
        "reponses": ['Je ne peux pas voir le ciel, mais j’espère qu’il fait beau !', 'Peut-être qu’il pleut, prends ton parapluie !']
    },
    "humour": {
        "mots": ['raconte une blague', 'blague', 'drôle'],
        "reponses": ['Pourquoi les poissons détestent l’ordinateur ? Parce qu’ils ont peur du net !', 'Qu’est-ce qui est jaune et qui attend ? Jonathan !']
    },
    "devinettes": {
        "mots": ['devinette', 'énigme', 'question difficile'],
        "reponses": ['Je suis toujours devant toi mais tu ne peux pas me voir. Qui suis-je ?', 'Plus je sèche, plus je deviens mouillé. Qu’est-ce que je suis ?']
    },
}


reponses_generiques = [
    "Intéressant…",
    "Hmm… je ne sais pas quoi répondre à ça.",
    "Peux-tu reformuler ?",
    "Je n'ai pas compris, peux-tu me le dire autrement ?",
    "Ah, je vois…"
]


def detecter_mot(question, list_mots) : 
    question_simplifier = unidecode.unidecode(question)
    for mot in list_mots : 
        mot_simplifier = unidecode.unidecode(mot)
        if mot_simplifier in question_simplifier : 
            return True
    return False

while True:
    question = input("Comment puis-je t'aider : ")
    nettoyer_question = question.lower().replace('?', '').replace('!', '').strip()
    
    if nettoyer_question == 'quit':
        print("Au revoir !")
        break
    trouver = False
    for categorie in base_AI.values() : 
        if detecter_mot(nettoyer_question, categorie['mots']) : 
            print(random.choice(categorie['reponses']))
            trouver = True
            break
    if not trouver : 
        print(random.choice(reponses_generiques))



    
