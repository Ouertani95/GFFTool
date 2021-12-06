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


def generateGraphGene():

    plt.bar(genePositions,geneTInt,label='Gene')
    plt.xlabel('Position')
    plt.ylabel('Taille (acide nucleique)')
    plt.title('Distribution de Taille')
    plt.legend(ncol=3,loc='upper right')
    plt.show()


def generateGraphIntron():

    plt.bar(intronPositions,intronTInt,label='Intron')
    plt.xlabel('Position')
    plt.ylabel('Taille (acide nucleique)')
    plt.title('Distribution de Taille')
    plt.legend(ncol=3,loc='upper right')
    plt.show()



def generateGraphInter():

    plt.bar(interPositions,interList,label='inter')
    plt.xlabel('Position')
    plt.ylabel('Taille (acide nucleique)')
    plt.title('Distribution de Taille')
    plt.legend(ncol=4,loc='upper right')
    plt.show()


def generateGraphFunc (window,resultsFrame):

    for widget in resultsFrame.winfo_children() :
        widget.destroy()
     
    window.geometry("730x350+350+0")

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
     #print(len(exonTInt))    

    global exonPositions 
    exonPositions = []
    for position in range(1,len(exonT)+1): 
        exonPositions.append(position)
     #print(len(exonPositions))
     #print(exonPositions)

    geneT= c.execute("SELECT end-start from features WHERE featuretype = 'gene' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

    global geneTInt
    geneTInt = []
    for geneLength in geneT :
        geneTInt.append(geneLength[0])
     
    global genePositions
    genePositions = []
    for position in range(1,len(geneT)+1): 
        genePositions.append(position)

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

    global startGene
    startGene = c.execute("SELECT start from features WHERE featuretype ='gene' and strand = '+' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

    global endGene 
    endGene = c.execute("SELECT end from features WHERE featuretype ='gene' and strand = '+' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

    interArray = np.column_stack((startGene,endGene))
    print(interArray)

    global interList
    interList = []
    for inter in range (1,len(interArray)) :
        interList.append(interArray[inter,0] - interArray[inter-1,1])
    print(interList)
     
    global interPositions
    interPositions = []
    for interStart in range(0,len(endGene)-1) : 
        interPositions.append(endGene[interStart][0]+1)

    print(interPositions)


    co.commit()
    c.close()
    co.close()

    exon_Button = ttk.Button(resultsFrame,text="Graphe d'exon",command=generateGraphExon)
    exon_Button.grid(column=1,row=1,pady=10,padx=25)

    gene_Button = ttk.Button(resultsFrame,text="Graphe des Genes",command=generateGraphGene)
    gene_Button.grid(column=1,row=0,pady=10,padx=25)

    intron_Button = ttk.Button(resultsFrame,text="Graphe des Introns ",command=generateGraphIntron)
    intron_Button.grid(column=2,row=0,pady=10,padx=25)

    inter_Button = ttk.Button(resultsFrame,text="Graphe des inter ",command=generateGraphInter)
    inter_Button.grid(column=2,row=1,pady=10,padx=25)
