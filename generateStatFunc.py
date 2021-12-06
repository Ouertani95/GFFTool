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



def resultGene() :

          # gene_Result = ttk.Label(resultsFrame,text= "Taille Moyenne Des Genes : " +geneAllMean)
          # gene_Result.grid(column=0, row=1,sticky=W)
     meanResult.pack_forget()
     meanResult.config(text= "Taille Moyenne Des Genes : " + geneAllMean)

     minResult.pack_forget()
     minResult.config(text=" Taille Minimale Des Genes : " + geneMin)

     maxResult.pack_forget()
     maxResult.config(text="Taille Maximale Des Genes : " + geneMax)

          # geneMin_Result = ttk.Label(resultsFrame,text=" Taille Minimale Des Genes : " +geneMin)
          # geneMin_Result.grid(column=0, row=2,sticky=W)

          # geneMax_Result = ttk.Label(resultsFrame,text= "Taille Maximale Des Genes : " +geneMax)
          # geneMax_Result.grid(column=0, row=3,sticky=W)




def resultExon() :

          # Result = ttk.Label(resultsFrame,text= " Taille Moyenne Des Exons : " +exonAllMean)
          # Result.grid(column=1,row=1,sticky=W)
     meanResult.pack_forget()
     meanResult.config(text= "Taille Moyenne Des Exons : " + exonAllMean)

     minResult.pack_forget()
     minResult.config(text=" Taille Minimale Des Exons : " + exonMin)

     maxResult.pack_forget()
     maxResult.config(text="Taille Maximale Des Exons : " + exonMax)
          # mini_Result = ttk.Label(resultsFrame,text= "Taille Minimale Des Exons : " +exonMin)
          # mini_Result.grid(column=1,row=2,sticky=W)   

          # max_Result = ttk.Label(resultsFrame,text= "Taille Maximale des Exons : " +exonMax)
          # max_Result.grid(column=1,row=3,sticky=W) 


def resultIntron() : 
          
          # intronMean_Result = ttk.Label(resultsFrame,text= "Taille Moyenne Des Introns : " +intronAllMean)
          # intronMean_Result.grid(column=2, row=1,sticky=W)
     meanResult.pack_forget()
     meanResult.config(text= "Taille Moyenne Des Introns : " + intronAllMean )

     minResult.pack_forget()
     minResult.config(text=" Taille Minimale Des Introns : " + intronMin)

     maxResult.pack_forget()
     maxResult.config(text="Taille Maximale Des Introns : " + intronMax)
     
          # intronMin_Result = ttk.Label(resultsFrame,text= "Taille Minimale Des Introns : " +intronMin)
          # intronMin_Result.grid(column=2, row=2,sticky=W)

          # intronMax_Result = ttk.Label(resultsFrame,text= "Taille Maximale Des Introns : " +intronMax)
          # intronMax_Result.grid(column=2, row=3,sticky=W)




def generatePiechartExonsIntrons ():

     global values 
     values = [intronPielist,exonPielist]
          
     global Names  
     Names = ["Intron","Exons"]
          
     plt.pie(values,labels=Names,autopct="%.1f%%",wedgeprops={'edgecolor':'white', 'linewidth':2})
     plt.title('Pourcentage Des Exons Et Introns')
     plt.show()


def generateStatFunc(window,resultsFrame):

     for widget in resultsFrame.winfo_children() :
          widget.destroy()
     
     window.geometry("730x380+350+0")
     
     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

     global meanResult
     meanResult = ttk.Label(resultsFrame,text="")
     meanResult.grid(column=1,row=1,pady=10,columnspan=3)

     global maxResult
     maxResult = ttk.Label(resultsFrame,text="")
     maxResult.grid(column=1,row=2,pady=10,columnspan=3)

     global minResult
     minResult = ttk.Label(resultsFrame,text="")
     minResult.grid(column=1,row=3,pady=10,columnspan=3)

     global geneAll 
     geneAll = c.execute("SELECT end-start from features WHERE featuretype = 'gene' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     
     geneAllArray = np.array(geneAll)
     global geneAllMean
     geneAllMean = round(geneAllArray.mean(),2)
     geneAllMean = str(geneAllMean)

     global geneMin
     geneMin = geneAllArray.min()
     geneMin = str(geneMin)

     global geneMax
     geneMax = geneAllArray.max()
     geneMax = str(geneMax)

     global exonAll
     exonAll = c.execute("SELECT end-start from features WHERE featuretype = 'exon'and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     
     exonAllArray = np.array(exonAll)
     global exonAllMean
     exonAllMean = round(exonAllArray.mean(),2)
     exonAllMean = str(exonAllMean)

     global exonMin
     exonMin = exonAllArray.min()
     exonMin= str(exonMin)

     global exonMax
     exonMax = exonAllArray.max()
     exonMax= str(exonMax)

     global intronAll
     intronAll= c.execute("SELECT end-start from features WHERE featuretype ='intron' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     
     intronAllArray = np.array(intronAll)

     global intronAllMean
     intronAllMean = round(intronAllArray.mean(),2)
     intronAllMean = str(intronAllMean)

     global intronMin
     intronMin = intronAllArray.min()
     intronMin = str(intronMin)

     global intronMax
     intronMax = intronAllArray.max()
     intronMax = str(intronMax)

     global intronPie
     intronPie = c.execute("SELECT count(end-start) from features WHERE featuretype ='intron' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     global intronPielist
     intronPielist = intronPie[0][0]

     global exonPie 
     exonPie = c.execute("SELECT count(end-start) from features WHERE featuretype ='exon' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     global exonPielist
     exonPielist = exonPie[0][0]

     co.commit()
     c.close()
     co.close()

     gene_Button = ttk.Button(resultsFrame,text="Stat Gene",command=resultGene)
     gene_Button.grid(column=0, row=1,padx=50,sticky=W)

     exon_Button = ttk.Button(resultsFrame,text="Stat exon",command=resultExon)
     exon_Button.grid(column=0, row=2,padx=50,sticky=W)

     intron_Button = ttk.Button(resultsFrame,text="Stat Intron",command=resultIntron)
     intron_Button.grid(column=0, row=3,padx=50,sticky=W)

     piechart_Button = ttk.Radiobutton(resultsFrame,text='PieChart',command=generatePiechartExonsIntrons)
     piechart_Button.grid(column=0,row=6,padx=30) 

     return    

     
