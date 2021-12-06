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


global window
window = themes.ThemedTk(theme="radiance")
window.geometry("730x230+350+0")
window.title("GFF Tool")
window.configure(bg="#F6F6F5")



def fileSelect():
     fileSelectFunc(window,selectedFile,resultsFrame,selectedRegion)

def region ():
     regionFunc(window,selectedRegion,resultsFrame,selectedFile)

def genesExons () : 
     genesExonsFunc(window,resultsFrame,selectedRegion)

def generateStat () : 
     generateStatFunc(window,resultsFrame,selectedRegion)

def generateGraph () : 
     generateGraphFunc(window,resultsFrame,selectedRegion)

selectionFrame = tk.Frame(window,background="#F6F6F5")
selectionFrame.grid(column=0,row=0,padx=5)


selectLabel = ttk.Label(selectionFrame,text="Sélectionner un fichier .GFF",foreground="black",background="#F6F6F5")
selectLabel.grid(column=0,row=0,padx=65,pady=5,sticky="W")
selectLocal = ttk.Button(selectionFrame,text="En local",command=fileSelect)
selectLocal.grid(column=0,row=1,padx=90,pady=5,sticky="W")
selectedFile = ttk.Label(selectionFrame,text="Aucun fichier sélectionné",background="#F6F6F5",foreground="#2E2E2E")
selectedFile.grid(column=0,row=2,padx=10,pady=5,ipadx=7)
selectOnline = ttk.Button(selectionFrame,text="En ligne",command=urlEntryFunc)
selectOnline.grid(column=0,row=3,padx=90,pady=5,sticky="W")
quitButton = ttk.Button(selectionFrame,text="Quitter", width=15, command=window.destroy)
quitButton.grid(column=0,row=4,padx=74,pady=5,sticky="W")



programFrame = tk.Frame(window,background="#F6F6F5")
programFrame.grid(column=1,row=0)


programLabel = ttk.Label(programFrame,text="Sélectionner un outil",foreground="black",background="#F6F6F5")
programLabel.grid(row=0,padx=120,pady=5,sticky=W)
genomicRegion = ttk.Radiobutton(programFrame,text="Définir une région génomique",value=1,command=region)
genomicRegion.grid(row=1,padx=50,pady=5,sticky=W)
selectedRegion = ttk.Label(programFrame,text="Aucune région sélectionnée",background="#F6F6F5",foreground="#2E2E2E")
selectedRegion.grid(row=2,padx=50,pady=11,sticky=W)
numberGenes = ttk.Radiobutton(programFrame,text="Récupérer nombre de gènes et exons",value=2,command=genesExons) 
numberGenes.grid(row=3,padx=50,pady=5,sticky=W)
graphGenerator = ttk.Radiobutton(programFrame,text="Générer des graphiques",value=3,command=generateGraph)
graphGenerator.grid(row=4,padx=50,pady=5,sticky=W)
statGenerator = ttk.Radiobutton(programFrame,text="Générer des statistiques",value=4,command=generateStat) 
statGenerator.grid(row=5,padx=50,pady=5,sticky=W)



resultsFrame=tk.Frame(window,background="#F6F6F5",height=450,width=700)# ,highlightbackground="#dd4814",highlightthickness=1
resultsFrame.grid(column=0,row=1,columnspan=2,pady=10,ipady=10)



window.mainloop()