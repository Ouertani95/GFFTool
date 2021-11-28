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

def regionFunc ():
     regionWindow = tk.Tk()
     regionWindow.geometry("650x350+700+100")
     regionWindow.title("GFF Region")

     chrScrollbar = tk.Scrollbar(regionWindow,orient=VERTICAL)
     startScrollbar = tk.Scrollbar(regionWindow,orient=VERTICAL)
     endScrollbar = tk.Scrollbar(regionWindow,orient=VERTICAL)

     chrLabel = tk.Label(regionWindow,text="Chromosome")
     chrLabel.grid (column=0,row=0,padx=20,pady=10)
     startLabel = tk.Label(regionWindow,text="Start")
     startLabel.grid (column=1,row=0,padx=20,pady=10)
     endLabel = tk.Label(regionWindow,text="End")
     endLabel.grid (column=2,row=0,padx=20,pady=10)

     
     chrChoice = tk.Listbox(regionWindow,yscrollcommand=chrScrollbar.set,exportselection=0)
     chrChoice.grid(column=0,row=1,padx=20,pady=10)
     
     for chromosome in fs.chrID :
          chrChoice.insert("end",chromosome)
     chrScrollbar.config(command=chrChoice.yview)
     chrScrollbar.grid(column=0,row=1,sticky='e''n''s')
     selectChr = chrChoice.get("anchor")
     print("le chromosome séléctionné est ",str(selectChr))
     def confirmerChoix():
          confChr = chrChoice.get(ANCHOR)
          return confChr
     confirmChr = tk.Button(regionWindow,text="Confirmer choix",command=confirmerChoix)

     #if selectChr != "" :
     
     startChoice = tk.Listbox(regionWindow,yscrollcommand=startScrollbar.set,exportselection=0)
     startChoice.grid(column=1,row=1,padx=20,pady=10)
     for start in fs.startList :
          startChoice.insert("end",start)
     startScrollbar.config(command=startChoice.yview)
     startScrollbar.grid(column=1,row=1,sticky='e''n''s')

    
     endChoice = tk.Listbox(regionWindow,yscrollcommand=endScrollbar.set,exportselection=0)
     endChoice.grid(column=2,row=1,padx=20,pady=10)
     for end in fs.endList :
          endChoice.insert("end",end)
     endScrollbar.config(command=endChoice.yview)
     endScrollbar.grid(column=2,row=1,sticky='e''n''s')

     def save ():
          global chrSelected
          chrSelected = "".join(chrChoice.get("anchor"))
          print(chrSelected)
          print(type(chrSelected))
          startTuple = startChoice.get("anchor")
          global startSelected
          startSelected = startTuple[0]
          print(startSelected)
          print(type(startSelected))
          endTuple = endChoice.get("anchor")
          global endSelected
          endSelected = endTuple[0]
          print(endSelected)
          print(type(endSelected))

          return

     SaveButton = tk.Button(regionWindow,text="Sauvegarder",command=save)
     SaveButton.grid(column=1,row=3,pady=10)
     regionQuitButton = tk.Button(regionWindow,text="Quitter",command=regionWindow.destroy)
     regionQuitButton.grid(column=1,row=4,pady=10)
