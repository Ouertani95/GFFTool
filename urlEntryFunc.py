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


def urlEntryFunc(window):
     urlEntry= tk.StringVar()
     entryLabel = tk.Label(window,text="Saisir l'url du fichier gff")
     entryLabel.grid(column=0,row=5)
     entryField = tk.Entry(window,textvariable=urlEntry)
     entryField.grid(column=0,row=6) 
     global wrongUrl
     wrongUrl = tk.Label(window,text="")
     wrongUrl.grid(column=0,row=8)
     def fileDownload ():
          urlLink = urlEntry.get()
          validUrl=validators.url(urlLink)
          print(validUrl)
          
          if validUrl!=True :
               #refresh entryField
               entryField.delete(0,tk.END)
               #remove old text from wrongUrl Label(used thanks to global outside of function)
               wrongUrl.pack_forget()
               wrongUrl.config(text="Url non valide")
          elif "gff" not in urlLink :
               #refresh entryField
               entryField.delete(0,tk.END)
               #remove old text from wrongUrl Label(used thanks to global outside of function)
               wrongUrl.pack_forget()
               wrongUrl.config(text="Pas de fichier gff trouvé")
          else :
               print(urlLink)
               #remove old text from wrongUrl Label(used thanks to global outside of function)
               wrongUrl.pack_forget()
               wget.download(url=urlLink)
               os.system("gzip -dk -f *.gz")
               wrongUrl.config(text="fichier téléchargé et dézippé ouvrir en local")
               
     
     downloadButton = tk.Button(window,text="Telecharger",command=fileDownload)
     downloadButton.grid(column=0,row=7)
      

