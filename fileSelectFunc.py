import tkinter as tk
from tkinter import StringVar, filedialog
from tkinter import font
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
from tkinter import messagebox

def fileSelectFunc(window,selectedFile,resultsFrame,selectedRegion) :
     """
     1) Shows file selection window from local repository
     2) Once file is selected verifies if database with the same name exists ; 
          if not creates database with same name as gff file
     3) Connects to database and recovers list of all chromosomes with all starts and ends available
     """
     for widget in resultsFrame.winfo_children() :
          widget.destroy()
     window.geometry("730x230+350+0")
     selectedRegion.pack_forget()
     selectedRegion.config(text="Aucune région sélectionnée",background="#F6F6F5",foreground="#2E2E2E")
     selectedFile.pack_forget()
     selectedFile.config(text="Aucun fichier sélectionné",background="#F6F6F5",foreground="#2E2E2E")

     #Afficher la fenêtre de selection du fichier gff en local
     window.filename = filedialog.askopenfilename(initialdir="~/Desktop/projetProgrammation2021",title="Selectionner un fichier gff",filetypes=(("gff files","*.gff"),("gff3 files",".gff3"),("gtf files","*.gtf"),("all files","*.*")))
     #extraire nom de fichier sans extension  à partir du fichier séléctionner en local 
     nameFile = Path(window.filename).stem
     print(nameFile)
     #créer nom de la base de données
     selectedFile.pack_forget()
     selectedFile.config(text=nameFile,foreground="#dd4814")
     global dbName
     dbName = nameFile + ".db"
     print(dbName)

     if os.path.exists(dbName)==False and nameFile!="":
     #créer la base de données si elle n'existe pas
          db = gffutils.create_db(window.filename, dbName)
          db = gffutils.FeatureDB(dbName)
          print("database created")
     if nameFile!="" :
          #se connecter à la base de données 
          con = sqlite3.connect(dbName)
          cur = con.cursor()
          #créer les listes de chromosomes, start et end à partir de la base de données créée
          global chrID
          chrID = cur.execute("SELECT DISTINCT seqid FROM features").fetchall()
          #chrID is a list of tuples
          print("chromosome list created")
          
          global startList
          startList = cur.execute("SELECT DISTINCT start FROM features ORDER BY start asc").fetchall()
          print ("start list created")
          
          global endList
          endList = cur.execute("SELECT DISTINCT end FROM features ORDER BY end desc").fetchall()
          print ("end list created")
          con.commit()
          cur.close()
          con.close()

     else : 
          messagebox.showwarning("Sélection fichier","Aucun fichier sélectionné")

     return

