import fileSelectFunc as fs
import urlEntryFunc as ue
import regionFunc as rf
import genesExonsFunc as ge
import generateGraphFunc as gg
import tkinter as tk
from tkinter import StringVar, filedialog
from tkinter.constants import ANCHOR, E, FALSE, LEFT, NS, NSEW, RAISED, RIGHT, VERTICAL, W, Y
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
#import statistics
import pymysql
import scipy as sp 
from scipy.stats import norm

def generateStatFunc ():
     statWindow = tk.Tk()
     statWindow.geometry("780x200+700+100")
     statWindow.title("GFF Stats")
     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

     global exonAll
     exonAll = c.execute("SELECT end-start from features WHERE featuretype = 'exon'and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     
     exonAllArray = np.array(exonAll)

     exonAllMean = round(exonAllArray.mean(),2)
     exonAllMean = str(exonAllMean)

     exonMin = exonAllArray.min()
     exonMin= str(exonMin)

     exonMax = exonAllArray.max()
     exonMax= str(exonMax)

     co.commit()
     c.close()
     co.close()


     def resultExon() :

          Result = tk.Label(statWindow,text= " Taille Moyenne Des Exons : " +exonAllMean)
          Result.grid(column=1,row=1)
     
          mini_Result = tk.Label(statWindow,text= "Taille Minimale Des Exons : " +exonMin)
          mini_Result.grid(column=1,row=2)   

          max_Result = tk.Label(statWindow,text= "Taille Maximale des Exons : " +exonMax)
          max_Result.grid(column=1,row=3) 

     exon_Button = tk.Button(statWindow,text="Stat exon",command=resultExon)
     exon_Button.grid(column=1, row=0, padx=80, pady= 10)
     #padx=10,pady=10,side=LEFT


     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

     global geneAll 
     geneAll = c.execute("SELECT end-start from features WHERE featuretype = 'gene' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     
     geneAllArray = np.array(geneAll)

     geneAllMean = round(geneAllArray.mean(),2)
     geneAllMean = str(geneAllMean)

     geneMin = geneAllArray.min()
     geneMin = str(geneMin)

     geneMax = geneAllArray.max()
     geneMax = str(geneMax)

     co.commit()
     c.close()
     co.close()

     def resultGene() :

          gene_Result = tk.Label(statWindow,text= "Taille Moyenne Des Genes : " +geneAllMean)
          gene_Result.grid(column=0, row=1)
     

          geneMin_Result = tk.Label(statWindow,text=" Taille Minimale Des Genes : " +geneMin)
          geneMin_Result.grid(column=0, row=2)

          geneMax_Result = tk.Label(statWindow,text= "Taille Maximale Des Genes : " +geneMax)
          geneMax_Result.grid(column=0, row=3)

     gene_Button = tk.Button(statWindow,text="Stat Gene",command=resultGene)
     gene_Button.grid(column=0, row=0,padx=80, pady= 10 )


     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

     global intronAll
     intronAll= c.execute("SELECT end-start from features WHERE featuretype ='intron' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     
     intronAllArray = np.array(intronAll)

     intronAllMean = round(intronAllArray.mean(),2)
     intronAllMean = str(intronAllMean)

     intronMin = intronAllArray.min()
     intronMin = str(intronMin)

     intronMax = intronAllArray.max()
     intronMax = str(intronMax)

     co.commit()
     c.close()
     co.close()

     def resultIntron() : 
          intronMean_Result = tk.Label(statWindow,text= "Taille Moyenne Des Introns : " +intronAllMean)
          intronMean_Result.grid(column=2, row=1)

     
          intronMin_Result = tk.Label(statWindow,text= "Taille Minimale Des Introns : " +intronMin)
          intronMin_Result.grid(column=2, row=2)

          intronMax_Result = tk.Label(statWindow,text= "Taille Maximale Des Introns : " +intronMax)
          intronMax_Result.grid(column=2, row=3)

     intron_Button = tk.Button(statWindow,text="Stat Intron",command=resultIntron)
     intron_Button.grid(column=2, row=0, padx=80, pady= 10)

     return    


#taille totale du chromosome 
#diagramme des % d'exon,intron,genes

     
