# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 18:36:48 2021

@author: Hp
"""

import csv
from numpy import argsort

nb_scores = 5
        
# fichier = open('ope.csv', 'w', newline='')
# champs = ["date","noeud","action","index","mineur","identifiant","prec"]
# writer = csv.DictWriter(fichier, fieldnames=champs)
# writer.writeheader()
        
fichier = open("scores.csv","r", newline='') #on recup les anciennes stats
lecteur = csv.DictReader(fichier) #scores est un tableau de strings
scores = [raw for raw in lecteur]
fichier.close()

def tri(e):
    return e['score']

print(scores)
scores = sorted(scores, key=lambda e: int(e['score']), reverse=True)

print(scores)

scores = scores

fichier = open('scores.csv', 'w', newline='') #et on va ecraser l'ancien fichier par un maj
champs = ["rang","score","nom","date"]
transcripteur = csv.DictWriter(fichier, fieldnames=champs)
transcripteur.writeheader()

for score in scores:
    machine.writerow({"rang":score[0], "score":score[1], "nom":score[2], "date":score[3]})
    