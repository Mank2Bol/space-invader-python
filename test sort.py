import csv

nb_scores = 5
        
fichier = open("scores.csv","r", newline='') #on recup les anciennes stats
lecteur = csv.DictReader(fichier) #scores est un tableau de strings
scores = [raw for raw in lecteur]
fichier.close()

scores = sorted(scores, key=lambda e: int(e['score']), reverse=True)

fichier = open('scores.csv', 'w', newline='') #et on va ecraser l'ancien fichier par un maj
champs = ["score","nom","date"]
transcripteur = csv.DictWriter(fichier, fieldnames=champs)
transcripteur.writeheader()
for score in scores:
    transcripteur.writerow({"score":score['score'], "nom":score['nom'], "date":score['date']})
fichier.close()
    