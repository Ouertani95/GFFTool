from re import X
import tkinter as tk
from tkinter import StringVar, Widget, filedialog
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

def customBar(current,total,width=80):
     """
     Shows download progress while file is downloading
     """
     print("Downloading: %d%% [%d / %d] bytes" % (current / total *100, current, total))
     downloadProgress["value"]=current / total *100
     wrongUrl.config(text=str(round(downloadProgress["value"]))+" % "+"["+str(current)+" / "+str(total)+"]" +" bytes",foreground="black")
     wrongUrl.pack()
     downloadWindow.update_idletasks()
     return

def fileDownload ():
     """
     Once downloadButton is pressed verifies the content of entryField :
     * Case 1 : entryField doesn't contain a valid url 
     => Changes label wrongUrl's text value to "Url non valide"
     * Case 2 : entryField contains a valid url but no gff file 
     => Changes label wrongUrl's text value to "Pas de fichier gff trouvé"
     * Case 3 : entryField contains a valid url and a gff file
     => Downloads file , decompresses downloaded file and changes label wrongUrl's text value to "Ouvrir le fichier en local"
     """
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
          print(urlLink)
          wget.download(url=urlLink,bar=customBar)
          print("fichier téléchargé")
          os.system("gzip -d -f *.gz")
          print("fichier dézippé")
          wrongUrl.pack_forget()
          wrongUrl.config(text="Ouvrir le fichier en local",foreground="#dd4814")
          wrongUrl.pack(pady=10)
     return

def urlEntryFunc():
     """
     Creates download window
     """

     global downloadWindow
     downloadWindow = tk.Toplevel()
     downloadWindow.geometry("410x190+670+0")
     downloadWindow.title("GFF Download")
     downloadWindow.configure(bg="#F6F6F5")

    
     entryLabel = tk.Label(downloadWindow,text="Saisir l'url du fichier gff",bg="#F6F6F5")
     entryLabel.pack(pady=10)

     global urlEntry
     urlEntry= tk.StringVar()
     global entryField
     entryField = ttk.Entry(downloadWindow,textvariable=urlEntry,width=35)
     entryField.pack(pady=5)
          
          
     downloadButton = ttk.Button(downloadWindow,text="Télécharger",command=fileDownload)
     downloadButton.pack(pady=5)

     global downloadProgress
     downloadProgress = ttk.Progressbar(downloadWindow,length=300,mode="determinate",orient=tk.HORIZONTAL)
     downloadProgress.pack(pady=5)
          
     global wrongUrl
     wrongUrl = ttk.Label(downloadWindow,text="")
     wrongUrl.pack(pady=5)

     # style = ttk.Style()
     # style.configure(downloadButton, font=('Helvetica', 16))
     # style.map(downloadButton,foreground=[('pressed', 'blue'),('active', 'red')])

     return