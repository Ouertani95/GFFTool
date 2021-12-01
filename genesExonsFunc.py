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
import tkinter.ttk as ttk 
import ttkthemes as themes


def genesExonsFunc():
     
     nbrWindow = themes.ThemedTk(theme="radiance")
     nbrWindow.geometry("550x150+700+100")
     nbrWindow.title("Region numbers")
     nbrWindow.configure(bg="#F6F6F5")

     global geneResult
     geneResult = ttk.Label(nbrWindow,text="")
     geneResult.grid(column=0,row=1,pady=10,columnspan=3)
     global exonResult
     exonResult = ttk.Label(nbrWindow,text="")
     exonResult.grid(column=0,row=2,pady=10,columnspan=3)

     def getPlus():

          con = sqlite3.connect(fs.dbName)
          cur = con.cursor()

          numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='gene' and strand = '+' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          numberGenes = numberGenesList[0][0]
          geneResult.pack_forget()
          geneResult.configure(text="Le nombre de gènes du brin + dans cette région est : "+str(numberGenes))
          

          numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and strand = '+' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          numberExons = numberExonsList[0][0]
          exonResult.pack_forget()
          exonResult.configure(text="Le nombre d'exons du brin + dans cette région est : "+str(numberExons))
          

          con.commit()
          cur.close()
          con.close()
          return

     plusButton = ttk.Button(nbrWindow,text="Brin +",command=getPlus)
     plusButton.grid(column=0,row=0,pady=10,padx=25)

     def getMinus():

          con = sqlite3.connect(fs.dbName)
          cur = con.cursor()

          numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='gene' and strand = '-' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          numberGenes = numberGenesList[0][0]
          geneResult.pack_forget()
          geneResult.configure(text="Le nombre de gènes du brin - dans cette région est : "+str(numberGenes))
         

          numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and strand = '-' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          numberExons = numberExonsList[0][0]
          exonResult.pack_forget()
          exonResult.configure(text="Le nombre d'exons du brin - dans cette région est : "+str(numberExons))
         

          con.commit()
          cur.close()
          con.close()
          return

     minusButton = ttk.Button(nbrWindow,text="Brin -",command=getMinus)
     minusButton.grid(column=1,row=0,pady=10,padx=25)

     def getBoth():

          con = sqlite3.connect(fs.dbName)
          cur = con.cursor()
          
          numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='gene' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          numberGenes = numberGenesList[0][0]
          geneResult.pack_forget()
          geneResult.configure(text="Le nombre total de gènes dans cette région est : "+str(numberGenes))
          
          
          numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          numberExons = numberExonsList[0][0]
          exonResult.pack_forget()
          exonResult.configure(text="Le nombre total d'exons dans cette région est : "+str(numberExons))
          
          
          con.commit()
          cur.close()
          con.close()
          
          return

     bothButton = ttk.Button(nbrWindow,text="2 Brins",command=getBoth)
     bothButton.grid(column=2,row=0,pady=10,padx=25)
