# coding: utf-8
 
from tkinter import * 
from math import *

user_data = int(input("\nHow many pages do you want on your website ?\n==> "))

fenetre = Tk()


for ligne in range(int(user_data/2)):
    for colonne in range(int(user_data/2)):
        Button(fenetre, text='L%s-C%s' % (ligne, colonne), borderwidth=1).grid(row=ligne, column=colonne)

for ligne in range(int(user_data/2)):
    for colonne in range(int(user_data/2)):
        Label(fenetre, text='L%s-C%s' % (ligne, colonne), borderwidth=1).grid(row=ligne+user_data, column=colonne)

Button(fenetre, text="Fermer", command=fenetre.quit, borderwidth=1).grid(row=user_data*2, column=user_data//4)

print(user_data//2)

# bouton de sortie
"""bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.pack()

label = Label(fenetre, text="Hello World")
label.pack()"""

fenetre.mainloop()