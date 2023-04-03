import numpy as np
import random
from tkinter import *



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


class TabMarkoff :
    def __init__(self,tab : [[]], states : []):
        self.tab = tab
        self.states = states
        self.previous_floor = 0

    def updateTab(self, destination : int):
        self.tab[self.previous_floor][destination].addUse()
        self.states[self.previous_floor].addUse(self.previous_floor,self.tab)
        self.previous_floor = destination

    def getTabText(self) :
        t = ""
        j = 0
        for i in self.tab :
            t += "\n"
            t += "state etage" + str(j) + ":"+ str(i)
            j += 1
        return t


class MarkoffModelWindow(Tk):
    def __init__(self,screenName: str | None = None, baseName: str | None = None, className: str = "Markoff Model", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.geometry("600x400")
        self.top_frame = Frame(self,bg='yellow')
        self.bottom_frame = Frame(self,bg='pink')
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=2, uniform="group1")
        self.grid_rowconfigure(1, weight=8, uniform="group1")
        self.grid_columnconfigure(0, weight=1)

        self.state_frame = Frame(self.top_frame, bg='yellow')
        self.buttons_frame = Frame(self.top_frame, bg='brown')
        self.state_frame.grid(row=0, column=0, sticky="nsew")
        self.buttons_frame.grid(row=1, column=0, sticky="nsew")
        self.top_frame.grid_rowconfigure(0, weight=1, uniform="group1")
        self.top_frame.grid_rowconfigure(1, weight=1, uniform="group1")
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.text_widget = Text(self.state_frame)
        self.text_widget.pack()
        new_text = "Nouveau texte"
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", new_text)

        self.tab_text = Text(self.bottom_frame)
        self.tab_text.pack()


    def setTabMarkoff(self,tabMarkoff : TabMarkoff):
        
        self.tabMarkoff = tabMarkoff
        self.index = 0
        btn1 = Button(self.buttons_frame ,text="State 0",command= self.actionState0, bg="gray")
        btn1.pack(side = LEFT,fill="x", expand=True)
        btn2 = Button(self.buttons_frame, text="State 1", command= self.actionState1, bg="gray")
        btn2.pack(side = LEFT,fill="x", expand=True)
        btn3 = Button(self.buttons_frame, text="State 2",command= self.actionState2, bg="gray")
        btn3.pack(side = LEFT,fill="x", expand=True)
        btn4 = Button(self.buttons_frame, text="State 3",command= self.actionState3, bg="gray")
        btn4.pack(side = LEFT,fill="x", expand=True)
        btn5 = Button(self.buttons_frame, text="State 4",command= self.actionState4, bg="gray")
        btn5.pack(side = LEFT,fill="x", expand=True)
    def actionState0(self):
        self.upadteInterface(0)

    def actionState1(self):
        self.upadteInterface(1)

    def actionState2(self):
        self.upadteInterface(2)

    def actionState3(self):
        self.upadteInterface(3)   

    def actionState4(self):
        self.upadteInterface(4) 

    def updateText(self,index: int):
        new_text = "Etage actuel : " + str(self.tabMarkoff.previous_floor) + " | Veuillez sélectionner l'étage de destination ( entre 0 et 4 ) "
        tab_updated = self.tabMarkoff.getTabText()
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", new_text)
        self.tab_text.delete("1.0", "end")
        self.tab_text.insert("1.0",tab_updated)

    def upadteInterface(self, index : int  ) :
        self.tabMarkoff.updateTab(index)
        self.updateText(index)




# Initialisation du modèle de Markov avec des valeurs nulles
tab = [[Cell() for i in range(5)] for j in range(5)]
states = [State() for i in range(5)]

new = MarkoffModelWindow()
new.setTabMarkoff(TabMarkoff(tab,states))
new.mainloop()
# Boucle principale pour les déplacements de l'utilisateur
"""while True:
    # Demander à l'utilisateur de choisir son prochain étage de destination
    destination = int(input("Etage actuel : " , previous_floor , "Entrez l'étage de destination (0-4) : "))
    
    # Mettre à jour la matrice de transition
    if previous_floor is not None:
        tab[previous_floor][destination].addUse()
        states[previous_floor].addUse(previous_floor,tab)



    j = 0
    new.upadteInterface(tab)
    for i in tab :
        print("")
        print( "state etage", j , ": ", i)
        j += 1
    
    previous_floor = destination
"""