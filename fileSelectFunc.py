from tkinter import filedialog
import os
import  gffutils
from pathlib import Path
import sqlite3
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

     #Shows file selection window from local repository
     window.filename = filedialog.askopenfilename(initialdir="~/Desktop/projetProgrammation2021",title="Selectionner un fichier gff",
     filetypes=(("gff files","*.gff"),("gff3 files",".gff3"),("gtf files","*.gtf"),("all files","*.*")))
     if (len(window.filename)) == 0 :
          messagebox.showwarning("Sélection fichier","Aucun fichier sélectionné")
     else : 
          global nameFile
          nameFile = Path(window.filename).stem #extracts file name without extension from selected local file
          selectedFile.pack_forget()
          selectedFile.config(text=nameFile,foreground="#dd4814")
          global dbName
          dbName = nameFile + ".db"
          if os.path.exists(dbName)==False :
               db = gffutils.create_db(window.filename, dbName) #create database
          
          con = sqlite3.connect(dbName)
          cur = con.cursor()
          global chrID
          chrID = cur.execute("SELECT DISTINCT seqid FROM features").fetchall()
               
          global startList
          startList = cur.execute("SELECT DISTINCT start FROM features ORDER BY start asc").fetchall()
               
          global endList
          endList = cur.execute("SELECT DISTINCT end FROM features ORDER BY end desc").fetchall()
          con.commit()
          cur.close()
          con.close()

     return