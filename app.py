
from flask import Flask, render_template, request, redirect, session, jsonify
import random
import unidecode
import json, os
import re
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


#-------memoire perssisstant-------#
memoire_utilisateur_file = 'memoire_utilisateur.json'
if os.path.exists(memoire_utilisateur_file) : 
    with open(memoire_utilisateur_file, 'r', encoding='utf-8') as f :
        memoire_utilisateur = json.load(f)
else : 
    memoire_utilisateur = {}

#-----------memoire perssisstant sauvegarde-----------#
def save_memoire_utilisateur() : 
    with open(memoire_utilisateur_file, 'w', encoding='utf') as f :
        json.dump(memoire_utilisateur, f, ensure_ascii=False, indent=2)


#------------ recuperer memoire utilisateur--------------#
def get_memoire_utilisateur(email):
    if email not in memoire_utilisateur:
        memoire_utilisateur[email] = {'nom': None, 'etat': None, 'preference': []}
    return memoire_utilisateur[email]


#--------fonction derniere reponse--------#
def choisir_reponse(categorie, mode):
    reponses = categorie['reponses_avance'] if mode == 'avance' and 'reponses_avance' in categorie else categorie['reponses']
    derniere_reponse = historique[-1]['reponse'] if historique else None
    reponses_possibles = [r for r in reponses if r != derniere_reponse]
    return random.choice(reponses_possibles) if reponses_possibles else random.choice(reponses)
#-----------reformulation------------#


def reformuler(reponse):
    # Nettoyer les ponctuations répétées
    propre = re.sub(r'[!?]+$', '', reponse.strip())

    variantes = [
        propre,
        propre + " 🙂",
        propre + " 😉",
        "Hmm… " + propre.lower(),
        propre + " ! Quoi de neuf ?",
        propre + " 😅",
        propre + " 😎",
        "Oh ! " + propre,
        "Intéressant ! " + propre
    ]

    return random.choice(variantes)


#-------------historique conversation retenu----------------#
memoire_ai = {}

if os.path.exists('memoire_calculs.json'):
    with open('memoire_calculs.json', 'r') as f:
        memoire_calcul = json.load(f)
else:
    memoire_calcul = {}


#-------------historique conversation----------------#
try:
    with open('historique.json', 'r', encoding='utf-8') as f:
        contenu = f.read().strip()
        if contenu:  # s'il y a du texte
            historique = json.loads(contenu)
        else:  # fichier vide
            historique = []
except FileNotFoundError:
    historique = []


#---------memoire AI-------------#

#--------------ajout utlisateur Json--------
users_file = 'users.json'
def loads_user() : 
    if os.path.exists(users_file) : 
        with open(users_file, 'r', encoding='utf-8') as f : 
            return json.load(f)
    return[]
def save_user(user) : 
    with open(users_file, 'w') as f : 
        json.dump(user, f , indent=4)




app.secret_key = '1346798520'
# _______________reponse AI _________
# ----------------- IA -----------------
def loads_ai_categories() : 
    with open('ai_categories.json', 'r', encoding='utf-8') as f : 
        return json.load(f)
    
base_AI = loads_ai_categories()

reponses_generiques = [
    "Intéressant…",
    "Hmm… je ne sais pas quoi répondre à ça.",
    "Peux-tu reformuler ?",
    "Je n'ai pas compris, peux-tu me le dire autrement ?",
    "Ah, je vois…"
]
#--------------reponse mots-------------
def detecter_mots(question, list_mots):
    question_simplifier = unidecode.unidecode(question)
    for mot in list_mots:
        mot_simplifier = unidecode.unidecode(mot)
        if mot_simplifier in question_simplifier:
            return True
    return False
memoire = {
    "nom": None,
    "preference": [],
    "etat": None
}
#---------------souvenir IA-----------#

def detecter_nom(question):
    email = session.get('email')
    memoire = get_memoire_utilisateur(email)
    save_memoire_utilisateur()

    match = re.search(r"je m'?appelle\s+([a-zA-Z]+)", question.lower())
    if match:
        nom = match.group(1).capitalize()
        memoire['nom'] = nom
        save_memoire_utilisateur()
        return f"Enchanté {nom} 😊"
    return None

def enregistrer_etat(question):
    email = session.get('email')
    memoire = get_memoire_utilisateur(email)

    if "je suis" in question:
        etat = question.split("je suis")[-1].strip()
        memoire['etat'] = etat
        save_memoire_utilisateur()
        return f"Merci, je note que tu es {etat}."
    return None

def repondre(question):
    mode = session.get('mode_chat', 'rapide')
    email = session.get('email')
    memoire = get_memoire_utilisateur(email)

    question = question.lower().replace("-", " ")

    # 1️⃣ Détection du nom
    reponse = detecter_nom(question)
    if reponse:
        ajouter_historique(question, reponse)
        return reponse

    # 2️⃣ Enregistrement de l'état si présent


def repondre(question):
    mode = session.get('mode_chat', 'rapide')
    email = session.get('email')
    memoire = get_memoire_utilisateur(email)

    question = question.lower().replace("-", " ")

    # 1️⃣ Détection du nom
    reponse = detecter_nom(question)
    if reponse:
        ajouter_historique(question, reponse)
        return reponse

    # 2️⃣ Enregistrement de l'état si présent
    reponse = enregistrer_etat(question)
    if reponse:
        ajouter_historique(question, reponse)
        return reponse

    # 3️⃣ Questions sur identité et état
    if "qui suis je" in question and memoire['nom']:
        reponse = f"Tu t'appelles {memoire['nom']} 😉"
        ajouter_historique(question, reponse)
        return reponse

    if "comment je vais" in question:
        if memoire['etat']:
            reponse = f"Tu m'avais dit que tu te sentais {memoire['etat']} 😊"
        else:
            reponse = "Ça va bien, merci et toi ?"
        ajouter_historique(question, reponse)
        return reponse

    if 'comment tu vas' in question or 'comment vas tu' in question:
        reponse = "Ça va bien, merci et toi ?"
        ajouter_historique(question, reponse)
        return reponse

    # 4️⃣ Vérification des catégories AI
    for categorie in base_AI.values():
        if detecter_mots(question, categorie['mots']):
            reponses = categorie.get('reponses_avance') if mode == 'avance' and 'reponses_avance' in categorie else categorie['reponses']
            reponse = random.choice(reponses)
            ajouter_historique(question, reponse)
            return reponse

    # 5️⃣ Réponse inconnue
    reponse = random.choice(
        base_AI['inconnu']['reponses_avance'] if mode == 'avance' else base_AI['inconnu']['reponses']
    )
    ajouter_historique(question, reponse)
    return reponse

#-------------mode AI-------------#
@app.route('/set_mode', methods=['POST'])
def set_mode():
    data = request.get_json()
    mode = data.get('mode', 'rapide')
    session['mode_chat'] = mode
    return jsonify({"mode": mode})


#------------ajouter a l'historique--------------#
def ajouter_historique(question, reponse):
    global historique
    historique.append({"question": question, "reponse": reponse})

    # Garder seulement les 50 derniers
    if len(historique) > 50:
        historique = historique[-50:]

    # Sauvegarde dans le fichier
    with open("historique.json", "w", encoding="utf-8") as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)
@app.route('/get_response')
def getresponse():
    global memoire_calcul
    global historique
    global memoire_ai

    question = request.args.get('question', '').strip()
    nettoyer_question = question.lower().replace('?', '').replace('!', '').strip()

    # 🔹 Cas spécial : effacer historique
    if nettoyer_question in ["efface historique", "reset", "vider mémoire"]:
        historique = []
        with open("historique.json", "w", encoding="utf-8") as f:
            json.dump(historique, f, ensure_ascii=False, indent=2)
        return "L'historique a été effacé ✅"

    # 🔹 Quitter
    if nettoyer_question == 'quit':
        return 'Au revoir !'

    # 🔹 Calculs
    if re.match(r'^[\d\s\+\-\*/x]+$', question):
        calcul = question.replace('x', '*')
        if calcul in memoire_calcul:
            return f"Je sais ! {calcul} = {memoire_calcul[calcul]}"
        try:
            resultat = eval(calcul, {"__builtins__": None}, {})
            memoire_calcul[calcul] = str(resultat)
            if len(memoire_calcul) > 50:
                memoire_calcul = dict(list(memoire_calcul.items())[-50:])
            with open('memoire_calculs.json', 'w') as f:
                json.dump(memoire_calcul, f, indent=2)
            return f"J'ai appris {calcul} = {resultat}"
        except:
            return "Je ne comprends pas ce calcul"

    # 🔹 Passer par la fonction principale de réponse
    reponse = repondre(question)
    return reponse







    
#--- page de connexion ---------
@app.route('/')
def index():
    if 'email' not in session:
        return redirect('/register')
    return render_template('index.html')

#-----------------se connecter-------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        users = loads_user()

        for user in users:
            if user.get('email') == email and user['password'] == password:
                session['email'] = email
                return redirect('/')
        return "Email ou mot de passe incorrect !"


    return render_template('login.html')

#----------------se deconnecter------------------
@app.route('/logout')
def logout() : 
    session.clear()
    return redirect('/login')


def email_exist(email, users): 
    """
    Vérifie si un email est déjà présent dans la liste d'utilisateurs.
    Retourne True si l'email existe, False sinon.
    """
    for user in users:
        if user['email'] == email:
            return True
    return False

def ajouter_utilisateur(email, password): 
    users = loads_user()
    if email_exist(email, users):  # ordre corrigé
        return False
    users.append({'email': email, 'password': password})
    save_user(users)
    return True

# ----------------- UTILISATEURS -----------------
#--------------enrigistrer utilisateur------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not ajouter_utilisateur(email, password):
            return "Cet email est déjà utilisé !"  # Bloque l'inscription si doublon

        session['email'] = email
        return redirect('/')

    return render_template('register.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render donne le port, sinon 5000 par défaut
    app.run(host="0.0.0.0", port=port, debug=True)

