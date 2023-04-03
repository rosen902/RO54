import numpy as np
import random

class State :
    def __init__ (self):
        self.useGlobale = 0
    def addUse(self, index : int ,cells : [[]]):
        self.useGlobale += 1
        for i in cells[index]:
            i.proba = i.use / self.useGlobale


class Cell: 
    def __init__ (self):
        self.use = 0
        self.proba = 0.0

    def __repr__ (self) :
        return "%.2f" % round(self.proba, 2)

    def __str__(self):
        return self.proba
        
    def addUse(self):
        self.use += 1

    def setProba(self, useGlobal) :
        self.proba = proba

# Initialisation du modèle de Markov avec des valeurs nulles
tab = [[Cell() for i in range(5)] for j in range(5)]
states = [State() for i in range(5)]
previous_floor = 0
turn = 0
# Boucle principale pour les déplacements de l'utilisateur
while True:
    # Demander à l'utilisateur de choisir son prochain étage de destination
    destination = int(input("Etage actuel : " , previous_floor , "Entrez l'étage de destination (0-4) : "))
    
    # Mettre à jour la matrice de transition
    if previous_floor is not None:
        tab[previous_floor][destination].addUse()
        states[previous_floor].addUse(previous_floor,tab)


    j = 0
    for i in tab :
        print("")
        print( "state etage", j , ": ", i)
        j += 1
    
    previous_floor = destination
