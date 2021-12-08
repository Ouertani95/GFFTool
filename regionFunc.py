from typing import Text
import fileSelectFunc as fs
import urlEntryFunc as ue
import genesExonsFunc as ge
import generateGraphFunc as gg
import generateStatFunc as gs
import tkinter as tk
from tkinter import Message, StringVar, filedialog
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
from tkinter import messagebox
import time

def getChr():
     """
     Once validateChr button is clicked :
     1) Recovers selected chromosome's value from chrChoice List box 
     2) Recovers all start and end positions relative to selected chromosome from database
     3) Modifies list boxes startChoice and endChoice to show only the new recovered start and end positions
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
     Once saveButton is clicked verifies if a value is selected from each list box :
     * Case 1 : at least one list box has no selected value 
     => Show warning messagebox to select all fields 
     * Case 2 : all list boxes have a selected value 
     => Modifies label selectionLabel text value to "Région sauvegardée" inside the tool's frame
     => Modifies label selectedRegion text value to the selected region inside the main window
     """

     if  chrChoice.get("anchor")=="" or startChoice.get("anchor")=="" or  endChoice.get("anchor")=="" :
          messagebox.showwarning("Selection de région","Veuillez sélectionner les 3 champs")
          # selectionLabel.pack_forget()
          # selectionLabel.config(text="Sélectionner les 3 champs",foreground="black")

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
          selectedRegionVar.config(text=chrSelected+" [ "+str(startSelected)+" , "+str(endSelected)+" ]",foreground="#dd4814")                   
     return

def regionFunc (window,selectedRegion,resultsFrame,selectedFile):
     """
     Verifies if a gff file is selected : 
     * Case 1 : no gff file is selected 
     => Shows messagebox with warning to select a gff file
     * Case 2 : a gff file is selected
     => Creates List boxes with all chromosome , start and end postions inside resultsFrame in main program window
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
               
