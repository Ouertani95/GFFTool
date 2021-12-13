import fileSelectFunc as fs
import regionFunc as rf
from tkinter.constants import CENTER
import numpy as np 
import sqlite3
import tkinter.ttk as ttk 
from tkinter import messagebox



def resultGene() :

     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

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
     

     co.commit()
     c.close()
     co.close()

     return geneMin,geneMax,geneAllMean



def resultExon() :

     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

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

     co.commit()
     c.close()
     co.close()

     return exonMin,exonMax,exonAllMean

def resultIntron() : 

     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

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

     co.commit()
     c.close()
     co.close()  

     return intronMin,intronMax,intronAllMean  

def resultIntergenes():

     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

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

     global interListMinus
     interListMinus = []
     for inter in range (1,len(interArrayMinus)) :
          if interArrayMinus[inter,0] - interArrayMinus[inter-1,1] < 0 :
               continue
          else : 
               interListMinus.append(interArrayMinus[inter,0] - interArrayMinus[inter-1,1])
               

     global interListBoth
     interListBoth = interListPlus + interListMinus
     print(interListBoth)

     interArray=np.array(interListBoth)

     global intergenesAllMean
     intergenesAllMean = round(interArray.mean(),2)
     intergenesAllMean = str(intergenesAllMean)

     global intergenesMin
     intergenesMin = interArray.min()
     intergenesMin = str(intergenesMin)

     global intergenesMax
     intergenesMax = interArray.max()
     intergenesMax = str(intergenesMax)
 

     co.commit()
     c.close()
     co.close() 

     return intergenesMin,intergenesMax,intergenesAllMean


def generateStatFunc(window,resultsFrame,selectedRegion):

     if selectedRegion.cget("text") == "Aucune région sélectionnée" or selectedRegion.cget("text") == "" : 
          messagebox.showwarning("Selection de région","Veuillez sélectionner une région")
     else :
          for widget in resultsFrame.winfo_children() :
               widget.destroy()
          
          window.geometry("730x450+350+0")

          graphTitle = ttk.Label(resultsFrame,text="Statistiques",foreground="black")
          graphTitle.grid(column=0,row=0,pady=15,columnspan=4)
          

          numbersTab = ttk.Treeview(resultsFrame,height=4)

          geneMin,geneMax,geneAllMean=resultGene()
          exonMin,exonMax,exonAllMean=resultExon()
          intronMin,intronMax,intronAllMean=resultIntron() 
          intergenesMin,intergenesMax,intergenesAllMean=resultIntergenes()

          
          #Define columns
          numbersTab["columns"] = ("Genes","Exons","Introns","Intergenes")

          numbersTab.column("#0",anchor=CENTER,width=120,minwidth=120)
          numbersTab.column("Genes",anchor=CENTER,width=120,minwidth=120)
          numbersTab.column("Exons",anchor=CENTER,width=120,minwidth=120)
          numbersTab.column("Introns",anchor=CENTER,width=120,minwidth=120)
          numbersTab.column("Intergenes",anchor=CENTER,width=120,minwidth=120)

          numbersTab.heading("#0",text="",anchor=CENTER)
          numbersTab.heading("Genes",text="Genes",anchor=CENTER)
          numbersTab.heading("Exons",text="Exons",anchor=CENTER)
          numbersTab.heading("Introns",text="Introns",anchor=CENTER)
          numbersTab.heading("Intergenes",text="Intergenes",anchor=CENTER)

          numbersTab.insert(parent="",index='end',iid=0,text="Minimum",value=(geneMin,exonMin,intronMin,intergenesMin))
          numbersTab.insert(parent="",index='end',iid=1,text="Maximum",value=(geneMax,exonMax,intronMax,intergenesMax))
          numbersTab.insert(parent="",index='end',iid=2,text="Mean",value=(geneAllMean,exonAllMean,intronAllMean,intergenesAllMean))
          
          numbersTab.grid(column=0,row=1,rowspan=1,columnspan=4)

     return    

     
