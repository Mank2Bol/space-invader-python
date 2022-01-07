import tkinter as tk
from random import randint
import keyboard.keyboard as kb
import threading as th
from math import exp
from time import sleep
import csv


class Jeu(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.iconbitmap('icon.ico')
        
        
        
        self.ecran_l = self.winfo_screenwidth()
        self.ecran_h = self.winfo_screenheight()
        self.hauteur_pan = 32+2*8
        self.hauteur = 480
        self.largeur = 830
        
        self.title("Gogo space Invaders")
        
        self.images = {'alien' : tk.PhotoImage(file='alien.gif'),
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

        self.score = 0 #score du joueur
        self.score_id = None
        self.texte_score = tk.StringVar() #var tk string du score du joueur maj avec fonction
        
        #self.vies = None vieux
        #self.vies_id =[] vieux
        

        self.niveau = 1
        
        self.unite = 8 #unite de pixel arbitraire comme pas de deplacement du vaisseau
        
        self.unite_image = 32
        self.liste_aliens = []
        self.vit_aliens = None # temps en ms entre chaque mouvement
        self.dirx = 10 # pas de deplacement, positif donc vers la droite (initialement)
        self.diry = 16 # pas de deplacement vers le bas
        self.avance = 0 #avancee des aliens
        
        self.largeur_tir = 4
        self.hauteur_tir = 10
        self.vit_tir =30 # temps en ms entre chaque mouvement
        self.diry_tir = 10 # les tir se deplacent par 10px
        self.queue_tir_joueur = [] #CONSIGNES j utilise bien une file dans le programme
        self.queue_tir_aliens = []
        self.periode_tirs = 1000 # en ms
        
        
        self.vaisseau = None
        self.tir_autorise = True
        self.actions_joueur = None
        self.tick = 1/50 # 50 ticks par seconde
        
        self.liste_murs = []
        
        
        self.ini_widgets()
        

        
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
        menu_jeu.add_command(label ='Nouvelle partie', command = self.commencer)
        menu_jeu.add_command(label ='Meilleurs scores', command = self.afficher_scores)
        menu_jeu.add_separator()
        menu_jeu.add_command(label='Quitter', command=self.quit)
        menu_barre.add_cascade(label ='Jeu', menu = menu_jeu)
        
        menu_options = tk.Menu(menu_barre, tearoff = 0)
        menu_barre.add_cascade(label ='Options', menu = menu_options)

        # menu_joueurs = tk.Menu(menu_options, tearoff = 0)
        
        # self.nombre_joueurs = tk.IntVar()
        # self.nombre_joueurs.set(1)
        # menu_joueurs.add_radiobutton(label='1 joueur', command = None, variable=self.nombre_joueurs, value=1)
        # menu_joueurs.add_radiobutton(label='2 joueur', command = None, variable=self.nombre_joueurs, value=2)
        # menu_options.add_cascade(label='Nombre de joueurs', menu=menu_joueurs)
        
        menu_options.add_command(label ='Controles', command = None)
        #menu_options.add_command(label ='Plein ecran', command = None)

        menu_barre.add_command(label ='A propos', command = None)
        
        htot = self.hauteur + self.hauteur_pan + 100
        geo = '+' + str(self.ecran_l//2 - self.largeur//2) + '+' + str((self.ecran_h - htot)//2)
        self.geometry(geo) #centrer la fenetre

    
    def afficher_scores(self):
        
        self.defaite()
        
        nb_scores = 5
        
# fichier = open('ope.csv', 'w', newline='')
# champs = ["date","noeud","action","index","mineur","identifiant","prec"]
# writer = csv.DictWriter(fichier, fieldnames=champs)
# writer.writeheader()
        
        fichier = open("scores.csv","r") #on recup les anciennes stats
        scores = csv.reader(fichier) #scores est un tableau de strings
        fichier.close()
        
        scores = scores[scores[:,2].argsort()]
        
        fichier = open('scores.csv', 'w', newline='') #et on va ecraser l'ancien fichier par un maj
        champs = ["rang","score","nom","date"]
        machine = csv.DictWriter(fichier, fieldnames=champs)
        machine.writeheader()
        
        
        
        for score in scores:
            machine.writerow({"rang":score[0], "score":score[1], "nom":score[2], "date":score[3]})
            
        
        
        popup = tk.Toplevel()
        popup.resizable(False, False)
        popup.title('Meilleurs scores')
        popup.transient(self) #reduction popup impossible 
        popup.grab_set() #interaction avec fenetre de jeu impossible
        
        
        frame = tk.Frame(popup)#, width=400, height=300)
        frame.grid(row=0, column=0, columnspan=3)
        
        tk.Button(popup,text='Fermer',command = popup.destroy).grid(row=1, column=0, padx=10, pady = 10)
        tk.Button(popup,text='Effacer',command = None).grid(row=1, column=1, padx=10, pady = 10)
        tk.Button(popup,text='Valider',command = None).grid(row=1, column=2, padx=10, pady = 10)
        
        tk.Label(frame, text='Rang').grid(row=0, column=0)
        for k in range(nb_scores): 
            tk.Label(frame, text=str(k+1)).grid(row=k+1, column=0)
        
        
        l = 500
        h = 500
        geo = '+' + str((self.ecran_l-l)//2) + '+' + str((self.ecran_h-h)//2) #centrer la fenetre popup
        popup.geometry(geo)
        self.wait_window(popup)
        fichier.close()
    
    def enregistrer_score(self):
        return
        

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
        
        coef = 1/10 #coed d adoucissement de l exp
        diff = exp(-coef*(1-self.niveau)) #difficultee du niveau
        
        self.vit_aliens = int( ( 975/54 * len(self.liste_aliens) + 25-975/54  ) * diff) #vitesse fonction lineaire du nombre d aliens pour un niveau donne

        if x_max >= self.largeur or x_min <= 0:
            self.dirx = -self.dirx #changement de sens de deplacement
            for alien in self.liste_aliens:
                alien.y = alien.y + self.diry
                self.can.coords(alien.id, alien.x, alien.y)

        if y_max >= self.hauteur - self.unite_image:
            self.defaite()
        
        for alien in self.liste_aliens:
            if alien.vivant:
                alien.x = alien.x + self.dirx
                self.can.coords(alien.id, alien.x, alien.y)
    
        self.after(self.vit_aliens, self.deplacement_aliens)

    def creation_aliens(self): # groupe d alien classique de 5 par 11, renvoie une liste d'objets Alien
        for i in range(5):
            for j in range(11):
                x = j * 40 + self.largeur//4
                y = i * 35
                self.liste_aliens.append( Entite(self, x, y, self.unite_image, self.images['alien'],False ))
    
    
    def creation_murs(self):
        for mur in self.liste_murs:
            mur.nettoyage()
        t = 16
        for i in range(4):
            x = self.largeur/8*(2*i+1)
            y = self.hauteur - self.unite_image - 8 #hauteur - taille mur - 8px
            self.liste_murs.append(Mur(self, x-2*t, y-3*t, t, t))
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
        #self.unbind('<space>')
        self.tir_autorise = False
        self.can.create_image(self.largeur//2, self.hauteur//2, anchor=tk.CENTER, image=self.images['defaite'])
        
    def niveau_suivant():
        return
        
    def chargement_niveau(self):
        nom = 'fond' + str( (self.niveau-1)%3+1 ) #trois images de fond seulement pour le moment
        self.can.create_image(0, 0, anchor=tk.NW, image=self.images[nom]) #image de fond du niveau

        self.creation_murs()
        
        
        

    def commencer(self):
        
        self.panneau = Panneau(self)
        
        self.chargement_niveau()
        
        self.vaisseau = Entite(self, self.largeur//2, self.hauteur-self.unite_image, self.unite_image, self.images['vaisseau'],True)

        self.creation_aliens()



        self.deplacement_aliens()
        self.tir_aliens()
        
        self.actions_joueur = ActionsJoueur(self) #thread avec boucle alternative

        
        
        #CHANGEMENT DE METHODE AVEC DU MULTITHREAD
        # self.bind('<Left>', self.deplacement_joueur)
        # self.bind('<Right>', self.deplacement_joueur)
        # self.bind('<space>', self.tir_joueur)


class Panneau():
    def __init__(self,jeu):
        self.jeu = jeu
        self.vies = 3
        self.vies_id = [self.jeu.pan.create_image(k*40+8, self.jeu.hauteur_pan/2-32/2, anchor=tk.NW, image=self.jeu.images['coeur']) for k in range(3)] #tableau avec id des images coeur
        self.score_id = self.jeu.pan.create_text(self.jeu.largeur-100, self.jeu.hauteur_pan/2, fill='white', font=('system',20), text='Score : 0')
        self.niveau_id = self.jeu.pan.create_text(self.jeu.largeur//2, self.jeu.hauteur_pan/2, fill='white', font=('system',20), text='Niveau 1')
    
    def malade(self):
        self.vies -=1
        self.jeu.pan.delete(self.vies_id[self.vies])
        if self.vies == 0:
            self.jeu.defaite()
            return False #mort
        return True #vivant
    
    def score_actualisation(self, points):
        self.jeu.score += points
        score_texte = 'Score : ' + str(self.jeu.score) + ' '
        self.jeu.pan.itemconfigure(self.score_id, text=score_texte)
    
    def niveau_actualisation(self):
        texte = 'Niveau : ' + str(self.jeu.niveau) + ' '
        self.jeu.pan.itemconfigure(self.niveau_id, text=texte) 


class Entite():
    def __init__(self,jeu,x,y,taille,photoimage,vaisseau):
        self.jeu = jeu
        self.x = x
        self.y = y
        self.l = taille
        self.h = taille
        self.vivant = True
        self.vaisseau = vaisseau
        
        #on créé l image sur le canvas qui renvoie l'identifiant
        # attention coin superieur gauche pour les coos (North West)
        self.id = jeu.can.create_image(x, y, image=photoimage, anchor=tk.NW)
    
    def destruction(self):
        id_explosion = jeu.can.create_image(self.x, self.y, image=self.jeu.images['explosion'], anchor=tk.NW)
        if self.vaisseau: #si l objet est le vaisseau du joueur
            self.vivant = self.jeu.panneau.malade()
            if not self.vivant:
                self.jeu.can.delete(self.id)
        else:
            self.vivant = False
            self.jeu.can.delete(self.id)
            self.jeu.panneau.score_actualisation(10)
            if len(self.jeu.liste_aliens) == 0:
                jeu.niveau_suivant()
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
        if self.vies > 0:
            photoimage = self.jeu.images['mur'+str(self.vies)]
            self.vies -= 1
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
            self.cibles = self.jeu.liste_aliens
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
            
            if kb.is_pressed('right'):
                self.jeu.droite()
            
            if kb.is_pressed('left'):
                self.jeu.gauche()
            
            if kb.is_pressed(' '):
                self.jeu.tir_joueur()
                
    def stop(self):
        self.actif = False
        print('THREAD TUE')

if __name__ == "__main__":
    jeu = Jeu()
    jeu.mainloop()
    jeu.actions_joueur.stop()
    jeu.destroy()







