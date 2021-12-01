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


def urlEntryFunc():

     downloadWindow = tk.Toplevel()
     downloadWindow.geometry("250x100+250+300")
     downloadWindow.title("GFF Region")

     urlEntry= tk.StringVar()
     entryLabel = tk.Label(downloadWindow,text="Saisir l'url du fichier gff")
     entryLabel.pack()
     #.grid(column=0,row=5)
     entryField = tk.Entry(downloadWindow,textvariable=urlEntry)
     entryField.pack()
     #.grid(column=0,row=6) 
     
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
               wrongUrl.pack()
          elif "gff" not in urlLink :
               #refresh entryField
               entryField.delete(0,tk.END)
               #remove old text from wrongUrl Label(used thanks to global outside of function)
               wrongUrl.pack_forget()
               wrongUrl.config(text="Pas de fichier gff trouvé")
               wrongUrl.pack()
          else :
               print(urlLink)
               #remove old text from wrongUrl Label(used thanks to global outside of function)
               wrongUrl.pack_forget()
               wget.download(url=urlLink)
               print("fichier téléchargé")
               os.system("gzip -dk -f *.gz")
               print("fichier dézippé")
               wrongUrl.config(text="Ouvrir fichier en local")
               wrongUrl.pack()

     
     downloadButton = tk.Button(downloadWindow,text="Telecharger",command=fileDownload)
     downloadButton.pack()
     #.grid(column=0,row=7)
     global wrongUrl
     wrongUrl = tk.Label(downloadWindow,text="")
     wrongUrl.pack()
     #.grid(column=0,row=8)