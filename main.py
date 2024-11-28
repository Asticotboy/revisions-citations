"""
@author : Cédric Ludwigs alias Asticotboy 

Le principe de ce script est simple :
Créer une interface agréable pour réviser les citations en français.
Les citations seront une par lignes dans un fichier citations.txt
Le programme ouvrira une interface web, et affichera une citation avec des mots manquants
Il faudra dans une zone de texte écrire la réponse.

Pour éviter les révisions inutiles, si les mots aléatoirement choisi sont des éléments d'une liste a_eviter, on change de mots 
"""

import random
import os
from flask import Flask, render_template, request
ponctuation = ["’", ",", ".", "!", "?", ":", ";", "(", ")", "[", "]", "{", "}","…", "–", "—", "«", "»", "\n", " ", "*"] 

a_eviter = [
            "le","de", "ROI", "la", "21", "-", "sept", "les", "contre", "thebes", "et", "un", "une", "des", "du", "dans", "par", "sur", "à", "qui", "que", "qu'", "qu’", "ce", "cette", "ces", "cet", "c'", "c’", "c", "d'", "d’", "d", "jusqu'",
            "en", 'thèbes', "(les", "thèbes)","chapitre", "Suppl"
            
            ]

a_eviter += ponctuation

for i in range(len(a_eviter)):
    a_eviter[i] = a_eviter[i].lower()
    
    
trou="_"
app = Flask(__name__, static_folder='static')

def get_citation():
    with open("citations.txt", "r", encoding="utf-8") as f:
        citations = f.readlines()
    return random.choice(citations)

def get_mots(citation, n=1):
    mots = citation.split(" ")
    
    mots = [mot for mot in mots if mot.lower() not in a_eviter]
    # Pour tous les mots, on enlève les caractères spéciaux
    mots_cool = []
    for i in range(len(mots)):
        if any(char.isdigit() for char in mots[i]):
            continue
        elif mots[i][0] == "X":
            continue
        
        else :
            for char in ponctuation[1:]:
                mots[i] = mots[i].replace(char, "")
            mots[i] = mots[i].replace("’", "'")
            if mots[i].lower() not in a_eviter:
                mots_cool.append(mots[i])
    mots_a_trouver = random.sample(mots_cool, n)
    for mot in mots_a_trouver:
        for p in ponctuation:
            for p2 in ponctuation:
                citation = citation.replace(p2+mot+p, " "+trou*len(mot)+" ")
    return mots_a_trouver, citation

citation = get_citation()
mots_a_trouver, citation = get_mots(citation, n=1)

@app.route("/", methods=["GET", "POST"])



def index():
    global citation, mots_a_trouver
    
    
    
    if request.method == "POST":
        reponses = request.form.get(f"reponse").split(" ")
        print(reponses)
        reponses = [reponse.lower() for reponse in reponses]
        mots_devais_trouver = [mot.lower() for mot in mots_a_trouver]
        print(mots_devais_trouver)
        success = False
        for reponse in reponses:
            if reponse in mots_devais_trouver:
                success = True
            else:
                success = False    
        
        citation = get_citation()
        mots_a_trouver, citation = get_mots(citation, n=2)
        
        return render_template("./index.html", citation=citation, mots_a_trouver=mots_a_trouver, mots_devais_trouver=mots_devais_trouver, success=success)
       
    print("Activé")
    
    citation = get_citation()
    mots_a_trouver, citation = get_mots(citation, n=2)
    
    return render_template("./index.html", citation=citation, mots_a_trouver=mots_a_trouver, success=None)

if __name__ == "__main__":
    app.run(debug=True)


