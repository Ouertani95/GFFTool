from fileSelectFunc import *
from urlEntryFunc import *
from regionFunc import *
from genesExonsFunc import *
from generateGraphFunc import *
from generateStatFunc import *
from re import A
import tkinter as tk
from tkinter import StringVar, filedialog
from tkinter.constants import ANCHOR, E, LEFT, NS, NSEW, RAISED, RIGHT, VERTICAL, W, Y
import wget
import validators
from glob import glob
import os
import numpy as np 
import matplotlib.pyplot as plt
import  gffutils
from gffutils.create import create_db
from pathlib import Path
import sqlite3
import pandas as pd
# import tkinter.ttk as ttk
# from PIL import Image 
# from PIL import ImageTk

global window
window = tk.Tk()
window.geometry("600x170")
window.title("GFF Tool")

#window.configure(bg="grey")
def fileSelect():
     
     fileSelectFunc(window)

# def urlEntry ():
#      urlEntryFunc(window)



programFrame = tk.Frame(window)
programFrame.grid(column=1,row=0,rowspan=20)


programLabel = tk.Label(programFrame,text="Sélectionner un outil")
programLabel.grid(row=0,padx=50,pady=5)
genomicRegion = tk.Radiobutton(programFrame,text="Définir une région génomique",value=1,command=regionFunc)
genomicRegion.grid(row=1,sticky=W,pady=5,padx=30)
numberGenes = tk.Radiobutton(programFrame,text="Récupérer nombre de gènes et exons",value=2,command=genesExonsFunc) 
numberGenes.grid(row=2,sticky=W,pady=5,padx=30)
graphGenerator = tk.Radiobutton(programFrame,text="Générer des graphiques",value=3,command=generateGraphFunc)
graphGenerator.grid(row=3,sticky=W,pady=5,padx=30)
statGenerator = tk.Radiobutton(programFrame,text="Générer des statistiques",value=4,command=generateStatFunc) 
statGenerator.grid(row=4,sticky=W,pady=5,padx=30)


selectLabel = tk.Label(window,text="Sélectionner un fichier .GFF")
selectLabel.grid(column=0,row=0,pady=5,padx=30)
selectLocal = tk.Button(window,text="En local",command=fileSelect)
selectLocal.grid(column=0,row=1,pady=5,padx=30)
selectOnline = tk.Button(window,text="En ligne",command=urlEntryFunc)
selectOnline.grid(column=0,row=2,pady=5,padx=30)


quitButton = tk.Button(window,text="Quitter", bg="sky blue", width=15, command=window.destroy)
quitButton.grid(column=0,row=10,pady=5,padx=30)


window.mainloop()