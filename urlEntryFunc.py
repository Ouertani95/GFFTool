from re import X
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


def urlEntryFunc():

     downloadWindow = tk.Toplevel()
     #themes.ThemedTk(theme="radiance")
     downloadWindow.geometry("410x195+450+100")
     downloadWindow.title("GFF Download")
     downloadWindow.configure(bg="#F6F6F5")

     urlEntry= tk.StringVar()
     entryLabel = tk.Label(downloadWindow,text="Saisir l'url du fichier gff",bg="#F6F6F5")
     entryLabel.pack(pady=10)
     #.grid(column=0,row=5)
     entryField = tk.Entry(downloadWindow,textvariable=urlEntry,bg="#F6F6F5",width=35)
     entryField.pack(pady=10)
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
               wrongUrl.pack(pady=10)
          elif "gff" not in urlLink :
               #refresh entryField
               entryField.delete(0,tk.END)
               #remove old text from wrongUrl Label(used thanks to global outside of function)
               wrongUrl.pack_forget()
               wrongUrl.config(text="Pas de fichier gff trouvé")
               wrongUrl.pack(pady=10)
          else :
               #remove old text from wrongUrl Label(used thanks to global outside of function)
               wrongUrl.pack_forget()
               wrongUrl.config(text="En cours de téléchargement")
               wrongUrl.pack(pady=10)
               print(urlLink)
               
               wget.download(url=urlLink)
               print("fichier téléchargé")
               os.system("gzip -dk -f *.gz")
               print("fichier dézippé")
               wrongUrl.pack_forget()
               wrongUrl.config(text="Ouvrir fichier en local",foreground="#dd4814")
               wrongUrl.pack(pady=10)

     
     downloadButton = tk.Button(downloadWindow,text="Telecharger",command=fileDownload,bg="#F6F6F5")
     downloadButton.pack(pady=10)
     #.grid(column=0,row=7)
     global wrongUrl
     wrongUrl = tk.Label(downloadWindow,text="",bg="#F6F6F5")
     wrongUrl.pack()
     #.grid(column=0,row=8)