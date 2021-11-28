import fileSelectFunc as fs
import urlEntryFunc as ue
import regionFunc as rf
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
from fileSelectFunc import *


def genesExonsFunc():
     #Anchor
     nbrWindow = tk.Tk()
     nbrWindow.geometry("400x100+700+100")
     nbrWindow.title("Region numbers")
     
     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='CDS' and start>=%s and end <=%s"%(rf.startSelected,rf.endSelected)).fetchall()
     numberGenes = numberGenesList[0][0]
     print(numberGenes)
     print(type(numberGenes))

     geneResult = tk.Label(nbrWindow,text="Le nombre de gènes dans cette région est : "+str(numberGenes))
     geneResult.grid(row=0,pady=10)

     numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and start>=%s and end <=%s"%(rf.startSelected,rf.endSelected)).fetchall()
     numberExons = numberExonsList[0][0]
     print(numberExons)
     print(type(numberExons))

     exonResult = tk.Label(nbrWindow,text="Le nombre d'exons dans cette région est : "+str(numberExons))
     exonResult.grid(row=1,pady=10)

     con.commit()
     cur.close()
     con.close()

