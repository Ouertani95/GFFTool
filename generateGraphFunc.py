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
from tkinter import messagebox
import matplotlib as mpl
from matplotlib import pylab
import seaborn as sns



def generateGraphExon ():

     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig1 = pylab.gcf()
     fig1.canvas.manager.set_window_title('Graphes Des Exons')
     plt.bar(exonPositions,exonTInt,label='exon',color='darkgrey')
          #plt.hist(geneT,label='gene')
          #plt.hist(intronT,label='intron')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de Taille Des Exons Sur Les 2 Brins',fontsize=13)
     plt.legend(ncol=3,loc='upper right')
          #bbox_to_anchor=(0.5,-0.1)
     plt.show()


def generateGraphGene():

     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig2 = pylab.gcf()
     fig2.canvas.manager.set_window_title('Graphes Des Genes')
     plt.bar(genePositions,geneTInt,label='Gene',color='chocolate')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de Taille Des Genes Sur Les 2 Brins',fontsize=13)
     plt.legend(ncol=3,loc='upper right')
     plt.show()


def generateGraphIntron():

     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig3 = pylab.gcf()
     fig3.canvas.manager.set_window_title('Graphes Des Introns')
     plt.bar(intronPositions,intronTInt,label='Intron',color='peru')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de Taille Des Introns Sur Les 2 Brins',fontsize=13)
     plt.legend(ncol=3,loc='upper right')
     plt.show()



def generateGraphInter():  

     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig1 = pylab.gcf()
     fig1.canvas.manager.set_window_title('Graphes Des Régions Intergéniques')
     plt.bar(interPositionsBoth,interListBoth,label='Régions Intergéniques',color='mediumseagreen')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de Taille Des Régions Intergéniques Sur Les 2 Brins',fontsize=11)
     plt.legend(ncol=4,loc='upper right')
     plt.show()

def generatePiechartExonsIntrons ():

     values = [sumIntrons,sumExons]
     Names = ["Introns","Exons"]
     col=['firebrick','darksalmon']
     
     figP = pylab.gcf()
     figP.canvas.manager.set_window_title('Distributions des Exons et des Intron')
     plt.pie(values,labels=Names,autopct="%.1f%%",wedgeprops={'edgecolor':'white', 'linewidth':2},colors=col)
     plt.title('Pourcentage Des Exons Et Introns')
     plt.show()

def generatePiechartGenesIntergeniques ():

     values1 = [sumGenes,sumInter]
     Names1 = ["Genes","Intergeniques"]
     col=['olive','yellowgreen']
     
     figP = pylab.gcf()
     figP.canvas.manager.set_window_title('Distributions des genes et des intergenes')
     plt.pie(values1,labels=Names1,autopct="%.1f%%",wedgeprops={'edgecolor':'white', 'linewidth':2},colors=col)
     plt.title('Pourcentage Des genes Et Intergenes')
     plt.show()


def generateBoxplot1() : 

     a = pd.DataFrame({ 'group' : np.repeat('Genes',len(geneTInt)), 'value': geneTInt })
     b = pd.DataFrame({ 'group' : np.repeat('Intergenes',len(interListBoth)), 'value': interListBoth })
     df=a.append(b)
     sns.boxplot(x='group', y='value', data=df,showmeans=True)
     plt.show()

def generateBoxplot2() : 

     c = pd.DataFrame({ 'group' : np.repeat('Exons',len(exonTInt)), 'value': exonTInt })
     d = pd.DataFrame({ 'group' : np.repeat('Introns',len(intronTInt)), 'value':intronTInt })
     df=c.append(d)
     sns.boxplot(x='group', y='value', data=df,showmeans=True)
     plt.show()

def generateGraphFunc (window,resultsFrame,selectedRegion):

     if selectedRegion.cget("text") == "Aucune région sélectionnée" or selectedRegion.cget("text") == "" : 
          messagebox.showwarning("Selection de région","Veuillez sélectionner une région")
     else :
          for widget in resultsFrame.winfo_children() :
               widget.destroy()
          
          window.geometry("730x550+350+0")

          mainTitle = ttk.Label(resultsFrame,text="Generation des graphes",foreground="black")
          mainTitle.grid(column=0,row=0,pady=15,columnspan=3)

          barTitle = ttk.Label(resultsFrame,text="Distribution des tailles",foreground="black")
          barTitle.grid(column=0,row=1,padx=20,pady=5)

          pieTitle = ttk.Label(resultsFrame,text="Proportions",foreground="black")
          pieTitle.grid(column=1,row=1,padx=20,pady=5)

          boxTitle = ttk.Label(resultsFrame,text="Comparaison des distributions",foreground="black")
          boxTitle.grid(column=2,row=1,padx=20,pady=5)

          # resultsFrame = themes.ThemedTk(theme="radiance")
          # resultsFrame.geometry("835x55+300+300")
          # resultsFrame.title("Generer Des Graphes")
          # resultsFrame.configure(bg="#F6F6F5")

          co= sqlite3.connect(fs.dbName)
          c = co.cursor()


          global exonT
          exonT= c.execute("SELECT end-start from features WHERE featuretype = 'exon' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          
          global exonTInt
          exonTInt = []
          for exonLength in exonT :
               exonTInt.append(exonLength[0])


          global exonPositions 
          exonPositions = []
          for position in range(1,len(exonT)+1): 
               exonPositions.append(position)

          global sumExons
          sumExons = 0
          for e in exonTInt :
               sumExons += e
          

          geneT= c.execute("SELECT end-start from features WHERE featuretype = 'gene' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          global geneTInt
          geneTInt = []
          for geneLength in geneT :
               geneTInt.append(geneLength[0])

          global genePositions
          genePositions = []
          for position in range(1,len(geneT)+1): 
               genePositions.append(position)

          global sumGenes
          sumGenes = 0
          for g in geneTInt :
               sumGenes+= g
          #print(sumGenes)


          global intronT
          intronT= c.execute("SELECT end-start from features WHERE featuretype ='intron' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          global intronTInt
          intronTInt = []
          for intronLength in intronT :
               intronTInt.append(intronLength[0])
          
          global intronPositions
          intronPositions = []
          for position in range(1,len(intronT)+1): 
               intronPositions.append(position)

          global sumIntrons
          sumIntrons = 0
          for s in intronTInt :
               sumIntrons += s
          #print(sumIntrons)    

          global startGenePlus
          startGenePlus = c.execute("SELECT start from features WHERE featuretype ='gene' and strand = '+' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          global endGenePlus
          endGenePlus= c.execute("SELECT end from features WHERE featuretype ='gene' and strand = '+' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          
          interArrayPlus = np.column_stack((startGenePlus,endGenePlus))

          global interListPlus
          interListPlus = []
          for inter in range (1,len(interArrayPlus)) :
               if interArrayPlus[inter,0] - interArrayPlus[inter-1,1] < 0 :
                    continue
               else :
                    interListPlus.append(interArrayPlus[inter,0] - interArrayPlus[inter-1,1])

          
          global interPositionsPlus
          interPositionsPlus = []
          for interStart in range(1,len(interListPlus)+1) : 
               interPositionsPlus.append(interStart)

     
          global startGeneMinus
          startGeneMinus= c.execute("SELECT start from features WHERE featuretype ='gene' and strand = '-' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          global endGeneMinus 
          endGeneMinus= c.execute("SELECT end from features WHERE featuretype ='gene' and strand = '-' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          interArrayMinus = np.column_stack((startGeneMinus,endGeneMinus))
          #print(interArrayMinus)

          global interListMinus
          interListMinus = []
          for inter in range (1,len(interArrayMinus)) :
               if interArrayMinus[inter,0] - interArrayMinus[inter-1,1] < 0 :
                    continue
               else : 
                    interListMinus.append(interArrayMinus[inter,0] - interArrayMinus[inter-1,1])
          

          global interListBoth
          interListBoth = interListPlus + interListMinus 

          #print(interListBoth)
          global sumInter
          sumInter = 0
          for v in interListBoth :
               sumInter+= v
          #print(sumInter)
          

          global interPielist
          interPielist = len(interListBoth)
 

          global interPositionsBoth
          interPositionsBoth = []
          for i in range(1,len(interListBoth)+1) : 
               interPositionsBoth.append(i)
  

          co.commit()
          c.close()
          co.close()

          exon_Button = ttk.Button(resultsFrame,text="Exons",command=generateGraphExon)
          exon_Button.grid(column=0,row=5,pady=10,padx=25)

          gene_Button = ttk.Button(resultsFrame,text="Genes",command=generateGraphGene)
          gene_Button.grid(column=0,row=2,pady=10,padx=25)

          intron_Button = ttk.Button(resultsFrame,text="Introns",command=generateGraphIntron)
          intron_Button.grid(column=0,row=4,pady=10,padx=25)

          inter_Button = ttk.Button(resultsFrame,text="Intergenes",command=generateGraphInter)
          inter_Button.grid(column=0,row=3,pady=10,padx=25)

          pie2_Button = ttk.Radiobutton(resultsFrame,text='Genes/Intergenes',command=generatePiechartGenesIntergeniques)
          pie2_Button.grid(column=1,row=2,padx=30,ipady= 25,sticky=W,rowspan=2) 

          pie1_Button = ttk.Radiobutton(resultsFrame,text='Exons/Introns',command=generatePiechartExonsIntrons)
          pie1_Button.grid(column=1,row=4,padx=30,ipady= 25,sticky=W,rowspan=2) 

          box1_Button = ttk.Button(resultsFrame,text='Boxplot G/I',command=generateBoxplot1)
          box1_Button.grid(column=2,row=2,padx=20,pady=5,rowspan=2)

          box2_Button = ttk.Button(resultsFrame,text='Boxplot E/I',command=generateBoxplot2)
          box2_Button.grid(column=2,row=4,padx=20,pady=5,rowspan=2)



     return