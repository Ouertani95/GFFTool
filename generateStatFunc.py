from tkinter.font import names
import fileSelectFunc as fs
import urlEntryFunc as ue
import regionFunc as rf
import genesExonsFunc as ge
import generateGraphFunc as gg
import tkinter as tk
from tkinter import StringVar, filedialog
from tkinter.constants import ANCHOR, E, FALSE, LEFT, NS, NSEW, RAISED, RIGHT, S, VERTICAL, W, Y
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
#import pymysql
import scipy as sp 
from scipy.stats import norm
import tkinter.ttk as ttk 
import ttkthemes as themes

def generateStatFunc (resultsFrame):

     for widget in resultsFrame.winfo_children() :
          widget.destroy()

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

          Result = ttk.Label(resultsFrame,text= " Taille Moyenne Des Exons : " +exonAllMean)
          Result.grid(column=1,row=1,sticky=W)
     
          mini_Result = ttk.Label(resultsFrame,text= "Taille Minimale Des Exons : " +exonMin)
          mini_Result.grid(column=1,row=2,sticky=W)   

          max_Result = ttk.Label(resultsFrame,text= "Taille Maximale des Exons : " +exonMax)
          max_Result.grid(column=1,row=3,sticky=W) 

     exon_Button = ttk.Button(resultsFrame,text="Stat exon",command=resultExon)
     exon_Button.grid(column=1, row=0,padx=50)


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

          gene_Result = ttk.Label(resultsFrame,text= "Taille Moyenne Des Genes : " +geneAllMean)
          gene_Result.grid(column=0, row=1,sticky=W)
     

          geneMin_Result = ttk.Label(resultsFrame,text=" Taille Minimale Des Genes : " +geneMin)
          geneMin_Result.grid(column=0, row=2,sticky=W)

          geneMax_Result = ttk.Label(resultsFrame,text= "Taille Maximale Des Genes : " +geneMax)
          geneMax_Result.grid(column=0, row=3,sticky=W)

     gene_Button = ttk.Button(resultsFrame,text="Stat Gene",command=resultGene)
     gene_Button.grid(column=0, row=0,padx=50)


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
          intronMean_Result = ttk.Label(resultsFrame,text= "Taille Moyenne Des Introns : " +intronAllMean)
          intronMean_Result.grid(column=2, row=1,sticky=W)

     
          intronMin_Result = ttk.Label(resultsFrame,text= "Taille Minimale Des Introns : " +intronMin)
          intronMin_Result.grid(column=2, row=2,sticky=W)

          intronMax_Result = ttk.Label(resultsFrame,text= "Taille Maximale Des Introns : " +intronMax)
          intronMax_Result.grid(column=2, row=3,sticky=W)

     intron_Button = ttk.Button(resultsFrame,text="Stat Intron",command=resultIntron)
     intron_Button.grid(column=2, row=0,padx=50)

     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

     global intronPie
     intronPie = c.execute("SELECT count(end-start) from features WHERE featuretype ='intron' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     intronPielist = intronPie[0][0]
 

     global exonPie 
     exonPie = c.execute("SELECT count(end-start) from features WHERE featuretype ='exon' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     exonPielist = exonPie[0][0]
  

     co.commit()
     c.close()
     co.close()

     def generatePiechartExonsIntrons ():

          global values 
          values = [intronPielist,exonPielist]
          
          global Names  
          Names = ["Intron","Exons"]
          
          plt.pie(values,labels=Names,autopct="%.1f%%",wedgeprops={'edgecolor':'white', 'linewidth':2})
          plt.show()

     piechart_Button = ttk.Radiobutton(resultsFrame,text='PieChart',command=generatePiechartExonsIntrons)
     piechart_Button.grid(column=1,row=4,padx=30)           
     
     return    


#taille totale du chromosome 
#diagramme des % d'exon,intron,genes

     
