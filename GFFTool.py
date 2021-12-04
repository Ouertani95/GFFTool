from ttkthemes.themed_tk import ThemedTk
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
import tkinter.ttk as ttk 
import ttkthemes as themes
# import tkinter.ttk as ttk
# from PIL import Image 
# from PIL import ImageTk

global window
window = themes.ThemedTk(theme="radiance")
window.geometry("1200x250")
window.title("GFF Tool")
window.configure(bg="#F6F6F5")

#window.configure(bg="grey")
def fileSelect():
     fileSelectFunc(window,selectedFile)

def region ():
     regionFunc(selectedRegion)

# def urlEntry ():
#      urlEntryFunc(window)



programFrame = ttk.Frame(window)
programFrame.grid(column=1,row=0,rowspan=20)


programLabel = ttk.Label(programFrame,text="Sélectionner un outil",foreground="black")
programLabel.grid(row=0,pady=5,padx=100)
genomicRegion = ttk.Radiobutton(programFrame,text="Définir une région génomique",value=1,command=region)
genomicRegion.grid(row=1,sticky=W,pady=5,padx=100)
selectedRegion = ttk.Label(programFrame,text=" ",foreground="#dd4814")
selectedRegion.grid(row=2,sticky=W,pady=5,padx=100)
numberGenes = ttk.Radiobutton(programFrame,text="Récupérer nombre de gènes et exons",value=2,command=genesExonsFunc) 
numberGenes.grid(row=3,sticky=W,pady=5,padx=100)
graphGenerator = ttk.Radiobutton(programFrame,text="Générer des graphiques",value=3,command=generateGraphFunc)
graphGenerator.grid(row=4,sticky=W,pady=5,padx=100)
statGenerator = ttk.Radiobutton(programFrame,text="Générer des statistiques",value=4,command=generateStatFunc) 
statGenerator.grid(row=5,sticky=W,pady=5,padx=100)


selectLabel = ttk.Label(window,text="Sélectionner un fichier .GFF",foreground="black")
selectLabel.grid(column=0,row=0,pady=5)
selectLocal = ttk.Button(window,text="En local",command=fileSelect)
selectLocal.grid(column=0,row=1,pady=5)
selectedFile = ttk.Label(window,text=" ",foreground="#dd4814")
selectedFile.grid(column=0,row=2,pady=5)
selectOnline = ttk.Button(window,text="En ligne",command=urlEntryFunc)
selectOnline.grid(column=0,row=3,pady=5)


quitButton = ttk.Button(window,text="Quitter", width=15, command=window.destroy)
#, bg="sky blue"
quitButton.grid(column=0,row=4,pady=5)


window.mainloop()