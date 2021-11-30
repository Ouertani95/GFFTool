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

def fileSelectFunc(window) :
     #Afficher la fenêtre de selection du fichier gff en local
     window.filename = filedialog.askopenfilename(initialdir="~/Desktop/projetProgrammation2021",title="Selectionner un fichier gff",filetypes=(("gff files","*.gff"),("gff3 files",".gff3"),("gtf files","*.gtf"),("all files","*.*")))
     #extraire nom de fichier sans extension  à partir du fichier séléctionner en local 
     nameFile = Path(window.filename).stem
     print(nameFile)
     #créer nom de la base de données 
     global dbName
     dbName = nameFile + ".db"
     print(dbName)

     if os.path.exists(dbName)==False :
     #créer la base de données 
          db = gffutils.create_db(window.filename, dbName)
          db = gffutils.FeatureDB(dbName)
          print("database created")
     
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

