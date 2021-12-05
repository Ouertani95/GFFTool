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


def genesExonsFunc(window,resultsFrame):

     for widget in resultsFrame.winfo_children() :
          widget.destroy()
     
     window.geometry("730x350+350+0")
     global geneResult
     geneResult = ttk.Label(resultsFrame,text="")
     geneResult.grid(column=0,row=1,pady=10,columnspan=3)
     global exonResult
     exonResult = ttk.Label(resultsFrame,text="")
     exonResult.grid(column=0,row=2,pady=10,columnspan=3)
     # global intronResult
     # intronResult = ttk.Label(resultsFrame,text="")
     # intronResult.grid(column=0,row=3,pady=10,columnspan=3)

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
          
          # numberIntronsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='intron' and strand = '+' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          # numberIntrons = numberIntronsList[0][0]
          # intronResult.pack_forget()
          # intronResult.configure(text="Le nombre d'introns du brin + dans cette région est : "+str(numberIntrons))

          con.commit()
          cur.close()
          con.close()
          return

     plusButton = ttk.Button(resultsFrame,text="Brin +",command=getPlus)
     plusButton.grid(column=0,row=0,padx=40,pady=10)

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

          # numberIntronsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='intron' and strand = '-' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          # numberIntrons = numberIntronsList[0][0]
          # intronResult.pack_forget()
          # intronResult.configure(text="Le nombre d'introns du brin - dans cette région est : "+str(numberIntrons))
         

          con.commit()
          cur.close()
          con.close()
          return

     minusButton = ttk.Button(resultsFrame,text="Brin -",command=getMinus)
     minusButton.grid(column=1,row=0,padx=40,pady=10)

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

          # numberIntronsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='intron' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          # numberIntrons = numberIntronsList[0][0]
          # intronResult.pack_forget()
          # intronResult.configure(text="Le nombre d'introns total dans cette région est : "+str(numberIntrons))
          
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

     bothButton = ttk.Button(resultsFrame,text="2 Brins",command=getBoth)
     bothButton.grid(column=2,row=0,padx=40,pady=10)