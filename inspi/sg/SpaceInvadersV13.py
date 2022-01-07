# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 13:34:27 2018

@author: noemie.rolland
"""

from  tkinter import *
import math,random
from random import randint,randrange

def Clavier(event): #Gestion de l'évenement Appui sur une touche du clavier
    global PosX,PosY
    touche=event.keysym
    #déplacement vers la droite
    if touche=='d' :
        if PosX<850:
            PosX+=10
    #déplacement vers la gauche
    if touche=='s' :
        if PosX>50:
            PosX-=10
    if touche=='l':
        CreationTir()
        MouvTir()
    #on dessine le vaisseau à sa nouvelle place
    Canevas.coords(Vaisseau,PosX,PosY)

"""
Programme création
"""

#Création de la fenêtre principale
Mafenetre=Tk()
Mafenetre.title('Space Invaders')

#Création du Canvas
Largeur=900
Hauteur=600
Canevas=Canvas(Mafenetre, height= Hauteur, width=Largeur,bg='white')
Fond=PhotoImage(file='Licorne2.gif')
Canevas.create_image(0,0,anchor=NW,image=Fond)

#Création vaisseau
Dab=PhotoImage(file='Vaisseau3.gif')
Vaisseau=""
Canevas.focus_set()
Canevas.bind('s',Clavier)
Canevas.bind('d',Clavier)
Canevas.bind('l',Clavier)

#Création ilots
Bloc=PhotoImage(file='Bloc2.gif')
def CreationIlots(X,Y):
    Ilot=Canevas.create_image(X,Y,anchor=NW,image=Bloc)
    return Ilot
Ilots=""

#Création aliens
Caca=PhotoImage(file='CacaMulti.gif')
def CreationAliens(X,Y):
    Alien=Canevas.create_image(X,Y,anchor=NW,image=Caca)
    return Alien
Aliens=""
TirAlien=[]

#Images
Bonus=PhotoImage(file='Bonus3.gif')
EnnemiBonus=""
Arc=PhotoImage(file='Laser4.gif')
Victoire=PhotoImage(file='Victoire3.gif')
Defaite=PhotoImage(file='Defaite2.gif')

Vies=3
Score=0
Morts=0


"""
Fonctions
"""

#Déplacement de l'alien
def deplacement():
    global X,Y,dX,dY,Largeur,Hauteur
    TailleAlien=50
    XP=Canevas.coords(Aliens[0][0])[0]
    XD=Canevas.coords(Aliens[0][-1])[0]
    #rebond à gauche
    if XP+dX<0:
        X=0
        dX=-dX
        Y+=TailleAlien
    #rebond à droite
    if XD+TailleAlien+dX>Largeur:
        X=Largeur-TailleAlien-500
        dX=-dX
        Y+=TailleAlien
    #nouvelle direction
    X=X+dX
    Y=Y+dY
    #affichage
    for i in range(len(Aliens)):
        for j in range(len(Aliens[i])):
            Canevas.coords(Aliens[i][j],X+j*100,Y+i*100)
    if Y>=700:
        Canevas.unbind('l')
        Canevas.create_image(0,0,anchor=NW,image=Defaite)
    #déplacement
    Mafenetre.after(40,deplacement)

def CreationEnnemiBonus():
    global EnnemiBonus
    Canevas.move(EnnemiBonus,-10,0)
    Canevas.after(50,CreationEnnemiBonus)

def CreationTir():
    global PosX,PosY,Laser,VerifLaser
    XLaser=PosX
    YLaser1=PosY
    Laser=Canevas.create_image(XLaser,YLaser1,image=Arc)
    Canevas.unbind('l')
    VerifLaser=True
    VerificationLaser()
    
def MouvTir():
    global touche,YLaser,Laser,VerifLaser
    if VerifLaser:
        if Canevas.coords(Laser)[1]<=0:
            Canevas.bind('l',Clavier)
            Canevas.delete(Laser)
            VerifLaser=False
        else :
            Canevas.move(Laser,0,-10)
            Mafenetre.after(10,MouvTir)
        
def VerificationLaser():
    global VerifLaser
    if VerifLaser:
        DestructionLaser()
        Mafenetre.after(50,VerificationLaser)

def CreationTirAlien():
    global Aliens,TirAlien,YAlien,TirAlien
    i=randint(0,len(Aliens)-1)
    j=randint(0,len(Aliens[i])-1)
    XAlien=Canevas.coords(Aliens[i][j])[0]
    YAlien=Canevas.coords(Aliens[i][j])[1]
    TirAlien.append(Canevas.create_rectangle(XAlien,YAlien,XAlien+10,YAlien+25,fill='pink'))
    DestructionTirAlien()
    Mafenetre.after(1000,CreationTirAlien)

def MouvTirAlien():
    global Aliens,TirAlien,YAlien
    for k in range(len(TirAlien)-1):
        if Canevas.coords(TirAlien[k])[1]==600:
            Canevas.delete(TirAlien[k])
            TirAlien.pop(k)
        else : 
            Canevas.move(TirAlien[k],0,10)
    Mafenetre.after(10,MouvTirAlien)

def DestructionLaser():
    global Laser,TirAlien,Aliens,Ilots,Vaisseau,VerifLaser,Score,Morts
    #on cherche les éléments qui ont la même position que le laser
    collision=False
    x1Laser=Canevas.coords(Laser)[0]
    y1Laser=Canevas.coords(Laser)[1]
    x2Laser=x1Laser+15
    y2Laser=y1Laser+45
    Impact1=Canevas.find_overlapping(x1Laser,y1Laser,x2Laser,y2Laser)
    #retourne la liste des éléments touchés
    #suppression des éléments qui sont entrés en collision
    for i in Impact1:
        for i1 in Ilots:
            if i==i1:
                Canevas.delete(i1)
                collision=True
                Score+=10
                x.set("Score: "+str(Score))
        for i2 in TirAlien:
            if i==i2:
                Canevas.delete(i2)
                collision=True
                Score+=20
                x.set("Score: "+str(Score))
        for i3 in Aliens:
            for j in i3:
                if i==j:
                    Canevas.delete(j)
                    collision=True
                    Score+=50
                    Morts+=1
                    x.set("Score: "+str(Score))
            if Morts==18:
                Canevas.create_image(0,0,anchor=NW,image=Victoire)
        if i==EnnemiBonus:
            Canevas.delete(EnnemiBonus)
            collision=True
            Score+=150
            x.set("Score: "+str(Score))
        if collision:
            Canevas.delete(Laser)
            VerifLaser=False
            Canevas.bind('l',Clavier)
            return VerifLaser

def DestructionTirAlien():
    global Laser,TirAlien,Aliens,Ilots,Vaisseau,VerifLaser,Vies
    Collision=False
    #on cherche les éléments qui ont la même position que les tirs des aliens
    if len(TirAlien)!=0:
        for j in TirAlien:
            n=Canevas.coords(j)
            x1TirAlien=Canevas.coords(j)[0]
            y1TirAlien=Canevas.coords(j)[1]
            x2TirAlien=Canevas.coords(j)[2]
            y2TirAlien=Canevas.coords(j)[3]
            Impact2=Canevas.find_overlapping(x1TirAlien,y1TirAlien,x2TirAlien,y2TirAlien) #retourne la liste des éléments touchés
            #suppression des éléments qui sont entrés en collision
            for k in Impact2:
                for k2 in Ilots:
                    if k==k2:
                        Collision=True
                        Canevas.delete(k)
                if k==Vaisseau:
                    Vies-=1
                    y.set("Vies restantes: "+str(Vies))
                    Collision=True
                if Collision:
                    Canevas.delete(j)
                    TirAlien.pop(TirAlien.index(j))
                    if Vies==0:
                        Canevas.delete(k)
                        Canevas.unbind('l')
                        Canevas.create_image(0,0,anchor=NW,image=Defaite)
    Mafenetre.after(10,DestructionTirAlien)

def Jeu():
    global PosX,PosY,X,Y,XP,YP,dX,dY,VerifLaser,YLaser,Vaisseau,Ilots,Aliens,EnnemiBonus,TirAlien,Vies,Score,Morts
    Canevas.delete(Vaisseau)
    for i in Ilots:
        Canevas.delete(i)
    for i in Aliens:
        Canevas.delete(i)
    Canevas.create_image(0,0,anchor=NW,image=Fond)
    Morts=0
    Vies=3
    y.set("Vies restantes: "+str(Vies))
    Score=0
    x.set("Score: "+str(Score))
    #Création vaisseau
    PosX=450
    PosY=500
    Vaisseau=Canevas.create_image(PosX,PosY,image=Dab)
    Canevas.bind('l',Clavier)
    #Création ilots de défense
    Ilots=[]
    XIlot=45
    YIlot=600
    for i in range (0,54):
        Ilots.append(CreationIlots(XIlot,YIlot))
        if XIlot==195 or XIlot==510:
            XIlot+=135
        if XIlot==825:
            XIlot=45
            YIlot+=30
        else :
            XIlot+=30
    #Création aliens
    Aliens=[[],[],[]]
    X=200
    Y=0
    for i in range (0,3):
        for j in range (2,8):
            Aliens[i].append(CreationAliens(j*100,i*100))
    #direction initiale
    dX=3
    dY=0
    for i in range (0,3):
        for j in range (0,6):
            Canevas.move(Aliens[i][j],dX,dY)

    EnnemiBonus=Canevas.create_image(900,20,anchor=NW,image=Bonus)
    #Conditions initiales
    VerifLaser=False
    YLaser=800
    #Lancement du jeu
    deplacement()
    CreationTirAlien()
    MouvTirAlien()
    Mafenetre.after(randrange(10000,30000,1000),CreationEnnemiBonus)


"""
Programme interface graphique
"""

#Création du bouton début jeu
BoutonJeu=Button(Mafenetre,text='Jouer',command = Jeu)

#Création bouton fermer
BoutonQuitter=Button(Mafenetre,text='Quitter',command=Mafenetre.destroy)

#Afichage score
x=StringVar()
x.set("Score: "+str(Score))
LabelScore=Label(Mafenetre,textvariable=x,fg='black',bg='white')

#Affichage vies
y=StringVar()
y.set("Vies restantes: "+str(Vies))
LabelVies=Label(Mafenetre,textvariable=y,fg='black',bg='white')

#Mise en page
LabelScore.grid(row=1,column=1,sticky=W)
LabelVies.grid(row=1,column=2,sticky=E)
Canevas.grid(row=2,column=1,rowspan=2)
BoutonJeu.grid(row=2,column=2)
BoutonQuitter.grid(row=3,column=2)

Jeu()
Mafenetre.mainloop()
