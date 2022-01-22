import tkinter as tk
from random import randint
import keyboard.keyboard as kb
import threading as th
from math import exp,log
from time import sleep, time
from datetime import date
import csv


class Jeu(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.iconbitmap('icon.ico')
        self.ecran_l = self.winfo_screenwidth()
        self.ecran_h = self.winfo_screenheight()
        self.hauteur_pan = 32+2*8
        self.hauteur = 480 #dimensions de la fenetre
        self.largeur = 830
        self.title("Gogo space Invaders")
        self.images = {'alien' : tk.PhotoImage(file='alien.gif'),
                       'alien2' : tk.PhotoImage(file='alien2.gif'),
                       'vaisseau' : tk.PhotoImage(file='vaisseau.gif'),
                       'defaite' : tk.PhotoImage(file='defaite.gif'),
                       'coeur' : tk.PhotoImage(file='coeur.gif'),
                       'explosion' : tk.PhotoImage(file='explosion.gif'),
                       'mur1' : tk.PhotoImage(file='mur1.gif'),
                       'mur2' : tk.PhotoImage(file='mur2.gif'),
                       'mur3' : tk.PhotoImage(file='mur3.gif'),
                       'mur4' : tk.PhotoImage(file='mur4.gif'),
                       'fond1': tk.PhotoImage(file='fond1.gif'),
                       'fond2': tk.PhotoImage(file='fond2.gif'),
                       'fond3': tk.PhotoImage(file='fond3.gif')
                       }

        self.nb_scores = 5
        self.nom_du_joueur = 'Michel'

        self.bouton_droite = 'right'
        self.bouton_gauche = 'left'
        self.bouton_tirer = 'up'

        self.image_fond = None

        self.score = 0 #compteur du score du joueur

        self.en_cours = True
        self.defaite_id = None

        self.niveau = 0
        
        self.unite = 8 #unite de longueur de deplacement
        self.unite_image = 32 #taille des images 32x32

        self.vaisseau = None
        self.liste_aliens = []
        self.alien2 = []
        self.liste_murs = []
        self.nombre_aliens = 0
        self.vit_aliens = None # temps en ms entre chaque mouvement
        self.vit_alien2 = 90
        self.dirx = 10 # pas de deplacement, positif donc vers la droite (initialement)
        self.diry = 16 # pas de deplacement vers le bas
        
        self.largeur_tir = 4
        self.hauteur_tir = 10
        self.vit_tir =30 # temps en ms entre chaque mouvement
        self.diry_tir = 10 # les tir se deplacent par 10px
        self.queue_tir_joueur = [] #FILE
        self.queue_tir_aliens = []
        self.periode_tirs = 1000 # en ms
        
        self.tir_autorise = True
        self.actions_joueur = None
        self.tick = 1/50 # 50 ticks par seconde

        
        self.ini_widgets()
        self.initialisation_jeu()
        

        
    def ini_widgets(self):

        frame1 = tk.Frame(self)
        frame1.pack(side=tk.BOTTOM)
        
        self.can = tk.Canvas(frame1, width=self.largeur, height=self.hauteur, bg='black') # cannevas
        self.can.pack(side = tk.BOTTOM)
        
        self.pan = tk.Canvas(frame1, height=self.hauteur_pan, bg='black') # panneau affichage
        self.pan.pack(side = tk.TOP, fill = tk.X)
        
        menu_barre = tk.Menu(self)
        self.config(menu = menu_barre)
        
        menu_jeu = tk.Menu(menu_barre, tearoff = 0)
        menu_jeu.add_command(label ='Nouvelle partie', command = self.nouvelle_partie)
        menu_jeu.add_command(label ='Meilleurs scores', command = self.afficher_scores)
        menu_jeu.add_separator()
        menu_jeu.add_command(label='Quitter', command=self.quit)
        menu_barre.add_cascade(label ='Jeu', menu = menu_jeu)
        
        menu_options = tk.Menu(menu_barre, tearoff = 0)
        menu_barre.add_cascade(label ='Options', menu = menu_options)
        
        menu_options.add_command(label ='Controles', command = self.selection_controles)
        #menu_options.add_command(label ='Plein ecran', command = None)

        menu_barre.add_command(label ='A propos', command = self.apropos)
        
        htot = self.hauteur + self.hauteur_pan + 100
        geo = '+' + str(self.ecran_l//2 - self.largeur//2) + '+' + str((self.ecran_h - htot)//2)
        self.geometry(geo) #centrer la fenetre

    def apropos(self):
        
        self.pile = [] #PILE
        popup = tk.Toplevel()
        popup.resizable(False, False)
        popup.title('Selection des controles')
        popup.transient(self) #reduction popup impossible 
        popup.grab_set() #interaction avec fenetre de jeu impossible

        tk.Label(popup, text='Code par Quentin et Leo').grid(row=0, column=0, columnspan = 3)

        def empile():
            if randint(1,10)<10:
                e = tk.Label(popup, text='     ', background='red')
                e.grid(row=len(self.pile)+2, column=1)
                self.pile.append(e)
            else:
                e = tk.Label(popup, text='     ', background='green')
                e.grid(row=len(self.pile)+2, column=1)
                self.pile.append(e)

        tk.Button(popup,text='Empiler', command = empile).grid(row=1, column=0, padx=10, pady = 10)
        def depile():
            if len(self.pile)>0:
                self.pile.pop(-1).destroy()

        tk.Button(popup,text='Retirer', command = depile).grid(row=1, column=1, padx=10, pady = 10)
        tk.Button(popup,text='Fermer',command = popup.destroy).grid(row=1, column=2, padx=10, pady = 10)
        l = 500
        h = 500
        geo = '+' + str((self.ecran_l-l)//2) + '+' + str((self.ecran_h-h)//2) #centrer la fenetre popup
        popup.geometry(geo)
        self.wait_window(popup)

    def selection_controles(self):

        popup = tk.Toplevel()
        popup.resizable(False, False)
        popup.title('Selection des controles')
        popup.transient(self) #reduction popup impossible 
        popup.grab_set() #interaction avec fenetre de jeu impossible
        def f_1():
            self.bouton_droite = 'right'
            self.bouton_gauche = 'left'
            self.bouton_tirer = 'up'
            popup.destroy()
        tk.Button(popup,text='< ^ >', command = f_1).pack(fill='x')
        def f_2():
            self.bouton_droite = 'd'
            self.bouton_gauche = 'q'
            self.bouton_tirer = ' '
            popup.destroy()
        tk.Button(popup,text='Q D Espace', command = f_2).pack(fill='x')
        l = 500
        h = 500
        geo = '+' + str((self.ecran_l-l)//2) + '+' + str((self.ecran_h-h)//2) #centrer la fenetre popup
        popup.geometry(geo)
        self.wait_window(popup)

    def enregistrer_score(self):
        
        popup = tk.Toplevel()
        popup.resizable(False, False)
        popup.title('Nom du joueur')
        popup.transient(self) #reduction popup impossible 
        popup.grab_set() #interaction avec fenetre de jeu impossible
        entree = tk.Entry(popup, width=15)
        entree.insert(0,self.nom_du_joueur)
        entree.pack()
        def fonction():
            self.nom_du_joueur = entree.get()
            popup.destroy()
        tk.Button(popup,text='Valider', command = fonction).pack()
        l = 500
        h = 500
        geo = '+' + str((self.ecran_l-l)//2) + '+' + str((self.ecran_h-h)//2) #centrer la fenetre popup
        popup.geometry(geo)
        self.wait_window(popup)



        fichier = open("scores.csv","r", newline='') #on recup les anciennes stats
        lecteur = csv.DictReader(fichier)
        scores = [raw for raw in lecteur]
        fichier.close()

        #ajouter un score avant le tri
        score = {"score": self.score, "nom": self.nom_du_joueur, "date": date.today()}
        scores.append(score)

        scores = sorted(scores, key=lambda e: int(e['score']), reverse=True)

        #suppr un score apres le tri
        if len(scores)>self.nb_scores:
            scores.pop()
        
        fichier = open('scores.csv', 'w', newline='') #et on va ecraser l'ancien fichier par un maj
        champs = ["score","nom","date"]
        transcripteur = csv.DictWriter(fichier, fieldnames=champs)
        transcripteur.writeheader()
        for score in scores:
            transcripteur.writerow({"score":score['score'], "nom":score['nom'], "date":score['date']})
        fichier.close()

        self.afficher_scores()
    
    def afficher_scores(self):

        fichier = open("scores.csv","r", newline='') #on recup les anciennes stats
        lecteur = csv.DictReader(fichier)
        scores = [raw for raw in lecteur]
        fichier.close()

        popup = tk.Toplevel()
        popup.resizable(False, False)
        popup.title('Meilleurs scores')
        popup.transient(self) #reduction popup impossible 
        popup.grab_set() #interaction avec fenetre de jeu impossible
        
        
        frame = tk.Frame(popup)#, width=400, height=300)
        frame.grid(row=0, column=0, columnspan=3)
        
        tk.Button(popup,text='Fermer',command = popup.destroy).grid(row=1, column=0, padx=10, pady = 10)

        def fonction():
            self.effacer_scores()
            popup.destroy()
        tk.Button(popup,text='Effacer',command = fonction).grid(row=1, column=1, padx=10, pady = 10)
        
        tk.Label(frame, text='Rang').grid(row=0, column=0)
        tk.Label(frame, text='Score').grid(row=0, column=1)
        tk.Label(frame, text='Nom').grid(row=0, column=2)
        tk.Label(frame, text='Date').grid(row=0, column=3)
        for k in range(len(scores)): 
            tk.Label(frame, text=str(k+1)).grid(row=k+1, column=0)
            tk.Label(frame, text=scores[k]['score']).grid(row=k+1, column=1)
            tk.Label(frame, text=scores[k]['nom']).grid(row=k+1, column=2)
            tk.Label(frame, text=scores[k]['date']).grid(row=k+1, column=3)
        
        
        l = 500
        h = 500
        geo = '+' + str((self.ecran_l-l)//2) + '+' + str((self.ecran_h-h)//2) #centrer la fenetre popup
        popup.geometry(geo)
        self.wait_window(popup)

    def effacer_scores(self):
        fichier = open('scores.csv', 'w', newline='') #et on va ecraser l'ancien fichier par un maj
        champs = ["score","nom","date"]
        transcripteur = csv.DictWriter(fichier, fieldnames=champs)
        transcripteur.writeheader()
        fichier.close()
        
    
    def incrementation_score(self, points):
        self.score += points
        self.panneau.actualisation_affichage_score()
    
    def chargement_alien2(self,temps):
        if time() > temps:
            photoimage = self.images['alien2']
            y = 0
            x = self.largeur
            self.alien2 = [Alien2(self,x,y,self.unite_image,photoimage)]
            self.deplacement_alien2()
        else:
            self.after(3000, self.chargement_alien2, temps)

    def deplacement_alien2(self):
        alien = self.alien2[0]
        if alien.vivant:
            if alien.x < - self.unite_image:
                alien.vivant = False
            alien.x = alien.x - 10
            self.can.coords(alien.id, alien.x, alien.y)
            self.after(self.vit_alien2, self.deplacement_alien2)
        else:
            self.chargement_alien2(time()+randint(20,60))
        

    def deplacement_aliens(self):
        
        x_max = 0 #initialisation le pire x_max
        x_min = self.largeur
        y_max = 4*35
        k=len(self.liste_aliens)-1
        while k>=0:
            alien = self.liste_aliens[k]
            if alien.vivant:
                x_max = max(x_max, alien.x + alien.l + 8)
                x_min = min(x_min, alien.x)
                y_max = max( y_max, alien.y )
            else:#profitons en pour faire du menage
                del self.liste_aliens[k] #suppr l objet de la liste
                #del alien # que fait cette instruction ? l objectif etant de supprimer le lien vers l instance
            k -= 1
        
        a = (exp(0.9)-exp(0.01))/54
        b = exp(0.01)-a
        x = self.nombre_aliens
        self.vit_aliens = int(   1000*(   log( a*x+b ) + 0.1*exp(1-self.niveau)))

        if x_max >= self.largeur or x_min <= 0:
            self.dirx = -self.dirx #changement de sens de deplacement
            for alien in self.liste_aliens:
                alien.y = alien.y + self.diry #deplacement vers le bas
                self.can.coords(alien.id, alien.x, alien.y)

        if y_max + self.unite_image*3 >= self.hauteur - self.unite_image and self.en_cours:
            self.defaite()
        
        for alien in self.liste_aliens:
            if alien.vivant:
                alien.x = alien.x + self.dirx
                self.can.coords(alien.id, alien.x, alien.y)
    
        self.after(self.vit_aliens, self.deplacement_aliens)

    def creation_aliens(self): # groupe d alien classique de 5 par 11
        self.nombre_aliens = 5*11
        for i in range(5):
            for j in range(11):
                x = j * 40 + self.largeur//4
                y = i * 35 + self.unite_image + int( 150*( 1-4/(3+self.niveau) ) )
                self.liste_aliens.append( Alien(self, x, y, self.unite_image, self.images['alien'] ))
    
    
    def creation_murs(self):
        for mur in self.liste_murs:
            mur.nettoyage()
        t = 16
        for i in range(4):
            x = self.largeur/8*(2*i+1)
            y = self.hauteur - self.unite_image - 8 #hauteur - taille mur - 8px
            self.liste_murs.append(Mur(self, x-2*t, y-3*t, t, t)) #desole flemme de faire une boucle
            self.liste_murs.append(Mur(self, x-1*t, y-3*t, t, t))
            self.liste_murs.append(Mur(self, x-0*t, y-3*t, t, t))
            self.liste_murs.append(Mur(self, x+1*t, y-3*t, t, t))
            self.liste_murs.append(Mur(self, x-2*t, y-2*t, t, t))
            self.liste_murs.append(Mur(self, x-1*t, y-2*t, t, t))
            self.liste_murs.append(Mur(self, x-0*t, y-2*t, t, t))
            self.liste_murs.append(Mur(self, x+1*t, y-2*t, t, t))
            self.liste_murs.append(Mur(self, x-2*t, y-1*t, t, t))
            self.liste_murs.append(Mur(self, x+1*t, y-1*t, t, t))

    @staticmethod
    def collision(obj1,obj2):#les rectangles se chevauchent ils ?
        return not( (obj2.x > obj1.x + obj1.l) or (obj2.x + obj2.l < obj1.x) or (obj2.y > obj1.y + obj1.h) or (obj2.y + obj2.h < obj1.y) )

    #ANCIENNE FONCTION MAINTENANT THREAD
    # def deplacement_joueur(self,event):
    #     touche = event.keysym
    #     if touche == 'Right' :
    #         if self.vaisseau.x < self.largeur - 16:
    #             self.vaisseau.x +=self.unite
    #     elif touche == 'Left' :
    #         if self.vaisseau.x > 16:
    #             self.vaisseau.x -= self.unite

    #     self.can.coords(self.vaisseau.id,self.vaisseau.x,self.hauteur-self.unite_image)

    def droite(self):
       if self.vaisseau.x + self.unite_image < self.largeur:
           self.vaisseau.x += self.unite
           self.can.coords(self.vaisseau.id,self.vaisseau.x,self.vaisseau.y)
    
    def gauche(self):
        if self.vaisseau.x >= self.unite:
            self.vaisseau.x -= self.unite
            self.can.coords(self.vaisseau.id,self.vaisseau.x,self.vaisseau.y)

    def tir_joueur(self):
        if self.tir_autorise:
            l = self.largeur_tir
            h = self.hauteur_tir
            x = self.vaisseau.x + jeu.unite_image//2 - l//2 #le tir est centre par rapport au vaisseau
            y = self.hauteur - h - self.unite_image #le tir commence devant le vaisseau (qui est en bas)
            joueur_tireur = True #les aliens sont cible
            self.queue_tir_joueur.append(Tir(self, x, y, l, h, joueur_tireur))
        
    def tir_aliens(self):
        n = len(self.liste_aliens)
        if n and self.en_cours:
            alien = self.liste_aliens[randint(0,n-1)]
            l = self.largeur_tir*2
            h = self.hauteur_tir
            x = alien.x + self.unite_image//2 - l//2
            y = alien.y + self.unite_image
            joueur_tireur = False #les aliens ne sont pas cible
            self.queue_tir_aliens.append(Tir(self, x, y, l, h, joueur_tireur))
        self.after(self.periode_tirs, self.tir_aliens)
        
    def nettoyage_tir(self,joueur_tireur):
        if joueur_tireur:
            self.queue_tir_joueur.pop(0)
        else:
            self.queue_tir_aliens.pop(0)
        #CONSIGNES : l objet tir doit etre supr quand il arrive en haut, attention, on ne suppr pas une instance, on suppr seulement toutes les var qui redirigent  vers l instance, et apres le "garbage collector" les suppr (quand il en a envie)
        
    def defaite(self):
        self.tir_autorise = False
        self.en_cours = False

        self.defaite_id = self.can.create_image(self.largeur//2, self.hauteur//2, anchor=tk.CENTER, image=self.images['defaite'])
        self.enregistrer_score()

        
    def chargement_niveau(self):
        self.niveau += 1
        self.panneau.actualisation_affichage_niveau()

        nom = 'fond' + str( (self.niveau-1)%3+1 ) #trois images de fond seulement pour le moment
        self.can.itemconfig(self.image_fond, image=self.images[nom]) #image de fond du niveau

        self.creation_murs() #supprime les anciens

        self.creation_aliens() #ne supprime pas les anciens



        
        
    def initialisation_jeu(self):
        self.panneau = Panneau(self)
        
        self.image_fond = self.can.create_image(0, 0, anchor=tk.NW, image=self.images['fond1']) #image de fond du niveau
        self.nouvelle_partie()

        self.deplacement_aliens()
        self.tir_aliens()

        self.chargement_alien2(time()+randint(20,60))

        self.actions_joueur = ActionsJoueur(self) #thread avec boucle alternative




    def nouvelle_partie(self):
        if self.defaite_id:
            self.can.delete(self.defaite_id)
            self.defaite_id = None
        self.en_cours = True
        self.score = 0
        self.niveau = 0
        self.incrementation_score(0)
        self.dirx = abs(self.dirx) #on remet le deplacement dans le bon sens
        self.tir_autorise = True
        self.panneau.vie_ini()
        for alien in self.liste_aliens:
            alien.vivant = False
            self.can.delete(alien.id)
        self.liste_aliens = []
        
        #for mur in self.liste_murs: deja fait ?
        #    mur.nettoyage()


        self.chargement_niveau()
        
        if self.vaisseau:
            self.can.delete(self.vaisseau.id)
        self.vaisseau = Vaisseau(self, self.largeur//2, self.hauteur-self.unite_image, self.unite_image)



class Panneau():
    def __init__(self,jeu):
        self.jeu = jeu
        self.vies_id = []
        self.score_id = self.jeu.pan.create_text(self.jeu.largeur-100, self.jeu.hauteur_pan/2, fill='white', font=('system',20), text='Score : 0')
        self.niveau_id = self.jeu.pan.create_text(self.jeu.largeur//2, self.jeu.hauteur_pan/2, fill='white', font=('system',20), text='Niveau 1')
        self.vie_ini()

    def vie_ini(self):
        self.vies = 3
        for vie in self.vies_id:
            self.jeu.pan.delete(vie)
        self.vies_id = [self.jeu.pan.create_image(k*40+8, self.jeu.hauteur_pan/2-32/2, anchor=tk.NW, image=self.jeu.images['coeur']) for k in range(3)] #tableau avec id des images coeur

    def malade(self):
        self.vies -= 1
        self.jeu.pan.delete(self.vies_id[self.vies])
        if self.vies == 0:
            self.jeu.defaite()
            return False #mort
        return True #vivant
    
    def actualisation_affichage_score(self):
        texte = 'Score : ' + str(self.jeu.score) + ' '
        self.jeu.pan.itemconfigure(self.score_id, text=texte)
    
    def actualisation_affichage_niveau(self):
        texte = 'Niveau : ' + str(self.jeu.niveau) + ' '
        self.jeu.pan.itemconfigure(self.niveau_id, text=texte) 


class Vaisseau():
    def __init__(self,jeu,x,y,taille):
        self.jeu = jeu
        self.x = x
        self.y = y
        self.l = taille
        self.h = taille
        self.vivant = True
        
        #on créé l image sur le canvas qui renvoie l'identifiant
        # attention coin superieur gauche pour les coos (North West)
        photoimage = self.jeu.images['vaisseau']
        self.id = jeu.can.create_image(x, y, image=photoimage, anchor=tk.NW)
    
    def destruction(self):
        id_explosion = jeu.can.create_image(self.x, self.y, image=self.jeu.images['explosion'], anchor=tk.NW)
        self.vivant = self.jeu.panneau.malade()
        if not self.vivant:
            self.jeu.can.delete(self.id)
        self.jeu.after(110, self.jeu.can.delete, id_explosion)


class Alien2():
    def __init__(self,jeu,x,y,taille,photoimage):
        self.jeu = jeu
        self.x = x
        self.y = y
        self.l = taille
        self.h = taille
        self.vivant = True
        
        self.id = jeu.can.create_image(x, y, image=photoimage, anchor=tk.NW)
    
    def destruction(self):
        if self.vivant:
            id_explosion = self.jeu.can.create_image(self.x, self.y, image=self.jeu.images['explosion'], anchor=tk.NW)
            self.vivant = False
            self.jeu.can.delete(self.id)
            self.jeu.incrementation_score(150)
            self.jeu.after(110, self.jeu.can.delete, id_explosion)
        

class Alien():
    def __init__(self,jeu,x,y,taille,photoimage):
        self.jeu = jeu
        self.x = x
        self.y = y
        self.l = taille
        self.h = taille
        self.vivant = True
        
        #on créé l image sur le canvas qui renvoie l'identifiant
        # attention coin superieur gauche pour les coos (North West)
        self.id = jeu.can.create_image(x, y, image=photoimage, anchor=tk.NW)
    
    def destruction(self):
        if self.vivant:
            id_explosion = self.jeu.can.create_image(self.x, self.y, image=self.jeu.images['explosion'], anchor=tk.NW)
            self.vivant = False
            self.jeu.nombre_aliens-=1
            self.jeu.can.delete(self.id)
            self.jeu.incrementation_score(10)
            if self.jeu.nombre_aliens == 0:
                self.jeu.liste_aliens = []
                self.jeu.chargement_niveau()
            self.jeu.after(110, self.jeu.can.delete, id_explosion)
        
class Mur():
    def __init__(self,jeu,x,y,largeur,hauteur):
        self.jeu = jeu
        self.x = x
        self.y = y
        self.l = largeur
        self.h = hauteur
        self.vivant = True
        self.vies = 4
        photoimage = self.jeu.images['mur4']

        self.id = jeu.can.create_image(self.x, self.y, image=photoimage, anchor=tk.NW)
    
    def destruction(self):
        self.jeu.can.delete(self.id)
        self.vies -= 1
        if self.vies > 0:
            photoimage = self.jeu.images['mur'+str(self.vies)]
            
            self.id = jeu.can.create_image(self.x, self.y, image=photoimage, anchor=tk.NW)
        else:
            self.vivant = False
    
    def nettoyage(self):
        self.vies = 0
        self.destruction()




class Tir():
    def __init__(self, jeu, x, y, largeur, hauteur, joueur_tireur):
        self.jeu = jeu
        self.vivant = True
        self.l = largeur
        self.h = hauteur
        self.x = x
        self.y = y
        self.joueur_tireur = joueur_tireur
        if self.joueur_tireur: #si les aliens sont cibles
            #self.jeu.unbind('<space>') #un seul tir à l ecran pour le joueur
            self.jeu.tir_autorise = False
            self.dir = -1 #tir vers le haut, y decroissant
            self.cibles = self.jeu.liste_aliens + self.jeu.alien2
        else: #si les aliens tirent, le vaisseau est la cible
            self.dir = 1
            self.cibles = [self.jeu.vaisseau]
        
        
        #on créé l image sur le canvas qui renvoie l'identifiant
        # attention coin superieur gauche pour les coos (North West)
        self.id = jeu.can.create_rectangle(self.x, self.y, self.x+self.l, self.y+self.h, fill='red')
        
        self.deplacement_tir()
    
    def deplacement_tir(self):
        if self.vivant:
            self.collision_tir()
        if self.vivant:
            self.y = self.y + self.jeu.diry_tir * self.dir
            self.jeu.can.coords(self.id,self.x,self.y, self.x+self.l, self.y+self.h)
            self.jeu.after(self.jeu.vit_tir, self.deplacement_tir)
    
    def collision_tir(self):
        if self.y > self.jeu.largeur+100 or self.y < 0: 
            self.destruction()
        else:
            cibles = self.cibles + self.jeu.liste_murs
            for cible in cibles:
                if cible.vivant and self.jeu.collision(cible, self):
                    cible.destruction()
                    self.destruction()
        
    def destruction(self):
        self.vivant = False
        if self.joueur_tireur:  #si le tir venait du joueur il peut tirer a nouveau
            #self.jeu.bind('<space>', self.jeu.tir_joueur)
            self.jeu.tir_autorise = True
        self.jeu.can.delete(self.id)
        #self.jeu.nettoyage_tir(self.joueur_tireur) #je n ai pas teste si ca fonctionne correctement, voir "garbage collector"

class ActionsJoueur():
    def __init__(self,jeu):
        self.jeu = jeu
        self.actif = True
        self.tick = self.jeu.tick
        self.thread = th.Thread(target=self.boucle, daemon=True)
        self.thread.start()

    def boucle(self):

        while self.actif:
            # self.der_tps = self.tps
            # self.tps = time()
            # delta = self.tps - self.der_tps - self.tick
            sleep(self.tick)
            # print(delta/self.tick)
            
            if kb.is_pressed(self.jeu.bouton_droite):
                self.jeu.droite()
            
            if kb.is_pressed(self.jeu.bouton_gauche):
                self.jeu.gauche()
            
            if kb.is_pressed(self.jeu.bouton_tirer):
                self.jeu.tir_joueur()
            
            if kb.is_pressed('t'):
                self.jeu.vit_tir = 3

                
    def stop(self):
        self.actif = False
        print('THREAD TUE')

if __name__ == "__main__":
    jeu = Jeu()
    jeu.mainloop()
    jeu.actions_joueur.stop()
    jeu.destroy()







