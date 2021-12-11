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
from tkinter import messagebox

def getPlus():
     """
     Retrieves number of genes and exons in the + strand inside selected chromosome region from the database.
     Modifies labels geneResult and exonResult text values to show retrieved numbers.
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='gene' and strand = '+' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberGenes = numberGenesList[0][0]
     geneResult.pack_forget()
     geneResult.configure(text="Gènes brin + : "+str(numberGenes))
               

     numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and strand = '+' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberExons = numberExonsList[0][0]
     exonResult.pack_forget()
     exonResult.configure(text="Exons brin + : "+str(numberExons))
               
     numberIntronsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='intron' and strand = '+' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberIntrons = numberIntronsList[0][0]
     intronResult.pack_forget()
     intronResult.configure(text="Introns brin + : "+str(numberIntrons))


     # selectedStrand.pack_forget()
     # selectedStrand.config(text="Brin +")

     con.commit()
     cur.close()
     con.close()
     return

def getMinus():
     """
     Retrieves number of genes and exons in the - strand inside selected chromosome region from the database.
     Modifies labels geneResult and exonResult text values to show retrieved numbers.
     """
     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='gene' and strand = '-' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberGenes = numberGenesList[0][0]
     geneResult.pack_forget()
     geneResult.configure(text="Gènes brin - : "+str(numberGenes))
          

     numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and strand = '-' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberExons = numberExonsList[0][0]
     exonResult.pack_forget()
     exonResult.configure(text="Exons brin - : "+str(numberExons))

     numberIntronsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='intron' and strand = '-' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberIntrons = numberIntronsList[0][0]
     intronResult.pack_forget()
     intronResult.configure(text="Introns brin - : "+str(numberIntrons))
      
     # selectedStrand.pack_forget()
     # selectedStrand.config(text="Brin -")

     con.commit()
     cur.close()
     con.close()
     return

def getBoth():
     """
     Retrieves number of genes and exons in both strands inside selected chromosome region from the database.
     Modifies labels geneResult and exonResult text values to show retrieved numbers.
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()
               
     numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='gene' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     global numberGenes
     numberGenes = numberGenesList[0][0]
     geneResult.pack_forget()
     geneResult.configure(text="Gènes 2 brins : "+str(numberGenes))
               
               
     numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     global numberExons
     numberExons = numberExonsList[0][0]
     exonResult.pack_forget()
     exonResult.configure(text="Exons 2 brins : "+str(numberExons))

     numberIntronsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='intron' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     global numberIntrons
     numberIntrons = numberIntronsList[0][0]
     intronResult.pack_forget()
     intronResult.configure(text="Introns 2 brins : "+str(numberIntrons))

     # selectedStrand.pack_forget()
     # selectedStrand.config(text="2 Brins") 
            
     # global exonsLength
     # exonsLength = cur.execute("SELECT end-start from features WHERE featuretype = 'exon'and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     # print(len(exonsLength))
     # exonsLengthList = []
     # for Lengths in range(0,len(exonsLength)) :
     #      exonsLengthList.append(exonsLength[Lengths][0])
     # print(exonsLengthList)
     # print(len(exonsLengthList))

     # exonsLengthSum = np.sum(exonsLengthList)
     # print(exonsLengthSum)

     # global intronsLength
     # intronsLength = cur.execute("SELECT end-start from features WHERE featuretype = 'intron' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     # print(len(intronsLength))
     # intronsLengthList = []
     # for Lengths in range(0,len(intronsLength)) :
     #      intronsLengthList.append(intronsLength[Lengths][0])
     # print(intronsLengthList)
     # print(len(intronsLengthList))

     # intronsLengthSum = np.sum(intronsLengthList)
     # print(intronsLengthSum)


     # # create data: an array of values
     # exonsIntons=[exonsLengthSum,intronsLengthSum]
     # exonsPercent = "Exons : " + str(round((exonsLengthSum *100) / (exonsLengthSum+intronsLengthSum),2)) + " %"
     # intronsPercent = "Introns : " + str(round((intronsLengthSum*100) / (exonsLengthSum+intronsLengthSum),2)) + " %"
     # percent = exonsPercent,intronsPercent
     # # Create a pieplot
     # plt.pie(exonsIntons,labels=percent, labeldistance=1.15,wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })
     # plt.title("Proportions des tailles d'exons et d'introns dans les gènes")
     # plt.show()

     con.commit()
     cur.close()
     con.close()     
     return

def genesExonsFunc(window,resultsFrame,selectedRegion):
     """
     Verifies if a chromosome region is selected : 
     * Case 1 : no region is selected 
     => Shows messagebox with warning to select a region 
     * Case 2 : a region is selected
     => Creates strand selection buttons inside resultsFrame in main program window
     """
     if selectedRegion.cget("text") == "Aucune région sélectionnée" or selectedRegion.cget("text") == "" : 
          messagebox.showwarning("Selection de région","Veuillez sélectionner une région")
     else :
          for widget in resultsFrame.winfo_children() :
               widget.destroy()
          
          window.geometry("730x450+350+0")

          genesExonsTitle = ttk.Label(resultsFrame,text="Nombre de gènes et d'exons",foreground="black")
          genesExonsTitle.grid(column=0,row=0,pady=15,columnspan=3)

          global geneResult
          geneResult = ttk.Label(resultsFrame,text="")
          geneResult.grid(column=1,row=2,pady=10,columnspan=1)
          global exonResult
          exonResult = ttk.Label(resultsFrame,text="")
          exonResult.grid(column=1,row=3,pady=10,columnspan=1)
          global intronResult
          intronResult = ttk.Label(resultsFrame,text="")
          intronResult.grid(column=1,row=4,pady=10,columnspan=1)

          global plusButton
          plusButton = ttk.Button(resultsFrame,text="Brin +",command=getPlus)
          plusButton.grid(column=0,row=1,padx=40,pady=10)

          global minusButton
          minusButton = ttk.Button(resultsFrame,text="Brin -",command=getMinus)
          minusButton.grid(column=1,row=1,padx=40,pady=10)

          global bothButton
          bothButton = ttk.Button(resultsFrame,text="2 Brins",command=getBoth)
          bothButton.grid(column=2,row=1,padx=40,pady=10)

          # global selectedStrand
          # selectedStrand = ttk.Label(resultsFrame,text="",foreground="black",font=(20))
          # selectedStrand.grid(column=0,row=2,rowspan=3)
     return