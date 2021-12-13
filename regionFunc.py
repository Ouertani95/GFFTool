import fileSelectFunc as fs
import tkinter as tk
from tkinter.constants import VERTICAL
import sqlite3
import tkinter.ttk as ttk 
from tkinter import messagebox

def getChr():
     """
     If chromosome list contains more than one chromosome :
     Once validateChr button is clicked, gets all start and end positions 
     relative to selected chromosome from database
     """
     chrSelected = "".join(chrChoice.get("anchor")) #get tuple element and transform into string

     startChoice.delete(0,"end")
     endChoice.delete(0,"end")

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     startListChr = cur.execute("SELECT DISTINCT start FROM features WHERE seqid = '%s' ORDER BY start asc"%chrSelected).fetchall()
     for start in startListChr :
          startChoice.insert("end",start)

     endListChr = cur.execute("SELECT DISTINCT end FROM features WHERE seqid = '%s' ORDER BY end desc"%chrSelected).fetchall()
     for end in endListChr :
          endChoice.insert("end",end)

     con.commit()
     cur.close()
     con.close()
     return

def save ():
     """
     Once saveButton is clicked :
     if all fields are selected shows "Région sauvegardée" else shows warning message to select all fields
     """

     if  chrChoice.get("anchor")=="" or startChoice.get("anchor")=="" or  endChoice.get("anchor")=="" :
          messagebox.showwarning("Selection de région","Veuillez sélectionner les 3 champs")

     elif chrChoice.get("anchor")!="" and startChoice.get("anchor")!="" and  endChoice.get("anchor")!="" :
                    
          global chrSelected
          chrSelected = ''.join(chrChoice.get("anchor"))

          startTuple = startChoice.get("anchor")
          global startSelected
          startSelected = startTuple[0]
                    
          endTuple = endChoice.get("anchor")
          global endSelected
          endSelected = endTuple[0]
          selectionLabel.pack_forget()
          selectionLabel.config(text="Région sauvegardée",foreground="#dd4814")
          selectedRegionVar.pack_forget()
          selectedRegionVar.config(text=chrSelected+"["+str(startSelected)+","+str(endSelected)+"]",foreground="#dd4814")                   
     return

def regionFunc (window,selectedRegion,resultsFrame,selectedFile):
     """
     Once regionButton is selected from main window :
     If file is already selected gets all chromosome , start and end postions from database 
     Else shows warning message to select a file
     """

     global selectedRegionVar
     selectedRegionVar=selectedRegion
     
     if selectedFile.cget("text") == "Aucun fichier sélectionné" or selectedFile.cget("text") == "" : 
          messagebox.showwarning("Selection de fichier","Veuillez sélectionner un fichier en local")
     else :
          for widget in resultsFrame.winfo_children() :
               widget.destroy()
          window.geometry("730x570+350+0")

          regionTitle = ttk.Label(resultsFrame,text="Selection de région",foreground="black")
          regionTitle.grid(column=0,row=0,pady=15,columnspan=3)

          chrScrollbar = ttk.Scrollbar(resultsFrame,orient=VERTICAL)
          startScrollbar = ttk.Scrollbar(resultsFrame,orient=VERTICAL)
          endScrollbar = ttk.Scrollbar(resultsFrame,orient=VERTICAL)

          chrLabel = ttk.Label(resultsFrame,text="Chromosome")
          chrLabel.grid (column=0,row=1,padx=20,pady=10)
          startLabel = ttk.Label(resultsFrame,text="Start")
          startLabel.grid (column=1,row=1,padx=20,pady=10)
          endLabel = ttk.Label(resultsFrame,text="End")
          endLabel.grid (column=2,row=1,padx=20,pady=10)

          global chrChoice
          chrChoice = tk.Listbox(resultsFrame,yscrollcommand=chrScrollbar.set,exportselection=0)
          chrChoice.grid(column=0,row=2,padx=20,pady=10)
          
          for chromosome in fs.chrID :
               chrChoice.insert("end",chromosome)

          chrScrollbar.config(command=chrChoice.yview)
          chrScrollbar.grid(column=0,row=2,sticky='e''n''s')

          global startChoice
          startChoice = tk.Listbox(resultsFrame,yscrollcommand=startScrollbar.set,exportselection=0)
          startChoice.grid(column=1,row=2,padx=20,pady=10)

          for start in fs.startList :
               startChoice.insert("end",start)
          
          startScrollbar.config(command=startChoice.yview)
          startScrollbar.grid(column=1,row=2,sticky='e''n''s')

          global endChoice
          endChoice = tk.Listbox(resultsFrame,yscrollcommand=endScrollbar.set,exportselection=0)
          endChoice.grid(column=2,row=2,padx=20,pady=10)

          for end in fs.endList :
               endChoice.insert("end",end)
          
          endScrollbar.config(command=endChoice.yview)
          endScrollbar.grid(column=2,row=2,sticky='e''n''s')

          saveButton = ttk.Button(resultsFrame,text="Sauvegarder",command=save)
          saveButton.grid(column=1,row=3,pady=10)

          global selectionLabel
          selectionLabel = ttk.Label(resultsFrame,text="")
          selectionLabel.grid(column=2,row=3,pady=10)

          if len(fs.chrID)>1 :
               validateChr = ttk.Button(resultsFrame,text="Valider Chromosome",command=getChr)
               validateChr.grid(column=0,row=3,padx=20,pady=10)
     return
               
