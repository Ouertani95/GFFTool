from typing import Text
import fileSelectFunc as fs
import urlEntryFunc as ue
import genesExonsFunc as ge
import generateGraphFunc as gg
import generateStatFunc as gs
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

def regionFunc (selectedRegion):
     regionWindow = themes.ThemedTk(theme="radiance")
     regionWindow.geometry("650x350+150+335")
     regionWindow.title("GFF Region")
     regionWindow.configure(bg="#F6F6F5")

     chrScrollbar = ttk.Scrollbar(regionWindow,orient=VERTICAL)
     startScrollbar = ttk.Scrollbar(regionWindow,orient=VERTICAL)
     endScrollbar = ttk.Scrollbar(regionWindow,orient=VERTICAL)

     chrLabel = ttk.Label(regionWindow,text="Chromosome")
     chrLabel.grid (column=0,row=0,padx=20,pady=10)
     startLabel = ttk.Label(regionWindow,text="Start")
     startLabel.grid (column=1,row=0,padx=20,pady=10)
     endLabel = ttk.Label(regionWindow,text="End")
     endLabel.grid (column=2,row=0,padx=20,pady=10)

     
     chrChoice = tk.Listbox(regionWindow,yscrollcommand=chrScrollbar.set,exportselection=0)
     chrChoice.grid(column=0,row=1,padx=20,pady=10)
     
     for chromosome in fs.chrID :
          chrChoice.insert("end",chromosome)

     chrScrollbar.config(command=chrChoice.yview)
     chrScrollbar.grid(column=0,row=1,sticky='e''n''s')

     global startChoice
     startChoice = tk.Listbox(regionWindow,yscrollcommand=startScrollbar.set,exportselection=0)
     startChoice.grid(column=1,row=1,padx=20,pady=10)

     for start in fs.startList :
          startChoice.insert("end",start)
     
     startScrollbar.config(command=startChoice.yview)
     startScrollbar.grid(column=1,row=1,sticky='e''n''s')

     global endChoice
     endChoice = tk.Listbox(regionWindow,yscrollcommand=endScrollbar.set,exportselection=0)
     endChoice.grid(column=2,row=1,padx=20,pady=10)

     for end in fs.endList :
          endChoice.insert("end",end)
     
     endScrollbar.config(command=endChoice.yview)
     endScrollbar.grid(column=2,row=1,sticky='e''n''s')

     if len(fs.chrID)>1 :

          def getChr():
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
          
          validateChr = ttk.Button(regionWindow,text="Valider Chromosome",command=getChr)
          validateChr.grid(column=0,row=3,padx=20,pady=10)

     def save ():

          

          if  chrChoice.get("anchor")=="" or startChoice.get("anchor")=="" or  endChoice.get("anchor")=="" :
               selectionLabel.pack_forget()
               selectionLabel.config(text="Sélectionner les 3 champs",foreground="black")

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
               selectedRegion.pack_forget()
               selectedRegion.config(text=chrSelected+" [ "+str(startSelected)+" , "+str(endSelected)+" ]" )               
         
          return

     SaveButton = ttk.Button(regionWindow,text="Sauvegarder",command=save)
     SaveButton.grid(column=1,row=3,pady=10)
     regionQuitButton = ttk.Button(regionWindow,text="Quitter",command=regionWindow.destroy)
     regionQuitButton.grid(column=1,row=4,pady=10)
     global selectionLabel
     selectionLabel = ttk.Label(regionWindow,text="")
     selectionLabel.grid(column=2,row=3,pady=10)
