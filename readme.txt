règles du jeu et les spécificités de votre implémentation, l’adresse de votre répertoire GIT, et où se trouvent les implémentations des structures de données demandées


Le principe est de détruire des vagues d'aliens au moyen d'un canon laser en se déplaçant horizontalement sur l'écran. Utiliser les flèches du clavier par défaut pour se déplacer et tirer.



Spécificité implémentation:

Ajout d'une boucle Actions_Joueur dans un fil d'execution alternatif qui permet à l'aide du module keyboard de savoir tout les delta temps quelle touche est pressée, deplacement/tir selon
Remplace la technique proposée par les professeurs : utiliser la méthode bind de tkinter qui permet d'appeler des focntion à chaque appui
Permet d'ajouter de la fluidité aux déplacements


Répertoire GIT:
https://github.com/Mank2Bol/space-invader-python.git


Structures de données demandées:
liste : self.liste_aliens = [] contient les aliens non bonus à l'écran
file : self.queue_tir_joueur une file qui permet de nettoyer les tirs un à un du joueur
pile : self.pile une pile inutile et indispensable à notre menu "à propos"




Structure du programme:

Classe Générale du jeu
	definition/initialisation variables
	initialisation widget tkinter
	apropos
	selections controles
	enregistrer scores
	afficher scores
	effacer scores
	incrementation score
	chargement alien2
	chargement alien
	deplacement alien2
	deplacement aliens
	creation aliens
	creation murs
	collision
	droite
	gauche
	tir joueur
	tir aliens
	nettoyage tir
	defaite
	chargement niveau
	initialisation jeu
	nouvelle partie

Classe Panneau, pour gérer le canvas secondaire d'affichage des vies, score
	initialisation
	vie initialisation
	malade
	actualisation affichage score
	actualisation affichage niveau

Classe Vaisseau
	initialisation
	destruction

Classe alien2
	initialisation
	destruction

Classe alien
	initialisation
	destruction

Classe mur
	initialisation
	destruction
	nettoyage

Classe tir
	initialisation
	deplacement tir
	collision tir
	destruction

Classe actions joueurs
	initialisation
	boucle
	stop









Lien utiles/utilisés :
https://www.delftstack.com/fr/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/
https://stackoverflow.com/questions/1078838/oop-choosing-objects
https://jeux.developpez.com/tutoriels/theorie-des-collisions/formes-2d-simples/
https://www.andoverpatio.co.uk/21/space-invaders/