import fileSelectFunc as fs
import urlEntryFunc as ue
import regionFunc as rf
import genesExonsFunc as ge
import generateStatFunc as gs
import tkinter as tk
from tkinter import Label, StringVar, filedialog
from tkinter.constants import ANCHOR, E, LEFT, NS, NSEW, RAISED, RIGHT, VERTICAL, W, Y
import wget
import validators
from glob import glob
import os
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.widgets import Button  
import  gffutils
from gffutils.create import create_db
from pathlib import Path
import sqlite3
import pandas as pd
import tkinter.ttk as ttk 
import ttkthemes as themes



def generateGraphFunc ():

     grapheWindow = themes.ThemedTk(theme="radiance")
     grapheWindow.geometry("615x55+700+100")
     grapheWindow.title("Generer Des Graphes")
     grapheWindow.configure(bg="#F6F6F5")

     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

     global exonT
     exonT= c.execute("SELECT end-start from features WHERE featuretype = 'exon' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     
     exonTInt = []
     for exonLength in exonT :
          exonTInt.append(exonLength[0])
     #print(len(exonTInt))    
     
     exonPositions = []
     for position in range(1,len(exonT)+1): 
          exonPositions.append(position)
     #print(len(exonPositions))
     
     #print(exonPositions)

     co.commit()
     c.close()
     co.close()
     
     def generateGraphExon ():

          plt.bar(exonPositions,exonTInt,label='exon')
          #plt.hist(geneT,label='gene')
          #plt.hist(intronT,label='intron')
          

          plt.xlabel('Position')
          plt.ylabel('Taille (acide nucleique)')
          plt.title('Distribution de Taille')
          plt.legend(ncol=3,loc='upper right')
          #bbox_to_anchor=(0.5,-0.1)
          plt.show()

     exon_Button = ttk.Button(grapheWindow,text="Graphe d'exon",command=generateGraphExon)
     exon_Button.grid(column=0,row=0,pady=10,padx=25)


     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

     global geneT
     geneT= c.execute("SELECT end-start from features WHERE featuretype = 'gene' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

     geneTInt = []
     for geneLength in geneT :
          geneTInt.append(geneLength[0])
     

     genePositions = []
     for position in range(1,len(geneT)+1): 
          genePositions.append(position)

     co.commit()
     c.close()
     co.close()

     def generateGraphGene():

          plt.bar(genePositions,geneTInt,label='Gene')
          plt.xlabel('Position')
          plt.ylabel('Taille (acide nucleique)')
          plt.title('Distribution de Taille')
          plt.legend(ncol=3,loc='upper right')
          plt.show()

     gene_Button = ttk.Button(grapheWindow,text="Graphe des Genes",command=generateGraphGene)
     gene_Button.grid(column=1,row=0,pady=10,padx=25)

     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

     global intronT
     intronT= c.execute("SELECT end-start from features WHERE featuretype ='intron' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

     intronTInt = []
     for intronLength in intronT :
          intronTInt.append(intronLength[0])
     

     intronPositions = []
     for position in range(1,len(intronT)+1): 
          intronPositions.append(position)

     co.commit()
     c.close()
     co.close()

     def generateGraphIntron():

          plt.bar(intronPositions,intronTInt,label='Intron')
          plt.xlabel('Position')
          plt.ylabel('Taille (acide nucleique)')
          plt.title('Distribution de Taille')
          plt.legend(ncol=3,loc='upper right')
          plt.show()

     intron_Button = ttk.Button(grapheWindow,text="Graphe des Introns ",command=generateGraphIntron)
     intron_Button.grid(column=2,row=0,pady=10,padx=25)

     return



