import fileSelectFunc as fs
import regionFunc as rf
import generateGraphFunc as gg
from tkinter.constants import CENTER
import numpy as np 
import sqlite3
import tkinter.ttk as ttk 
from tkinter import messagebox



def resultFeature(feature) :
     """
     Retrieves all the features present in the chromosome in an array and then calculates the mean,minimum,and maximum
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     featureAll = cur.execute("SELECT end-start from features WHERE featuretype = '%s' and seqid='%s' and start >=%s and end<=%s"%(feature,rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          
     featureAllArray = np.array(featureAll)
     if len(featureAllArray) !=0 :
          geneAllMean = round(featureAllArray.mean(),2)

          geneMin = featureAllArray.min()

          geneMax = featureAllArray.max()
     else :
          geneAllMean=0
          geneMin=0
          geneMax=0
     
     con.commit()
     cur.close()
     con.close()
     return geneMin,geneMax,geneAllMean


def resultIntergenes():
     """
     Retrieves all the intergenes present in the chromosome and then calculates the mean,minimum,and maximum
     """

     interListBoth,sumInter,interPositionsBoth=gg.calculIntergenes()

     interArray=np.array(interListBoth)
     if len(interArray) != 0 :  
          intergenesAllMean = round(interArray.mean(),2)

          intergenesMin = interArray.min()

          intergenesMax = interArray.max() 
     else :
          intergenesAllMean=0
          intergenesMin=0
          intergenesMax=0 

     return intergenesMin,intergenesMax,intergenesAllMean


def generateStatFunc(window,resultsFrame,selectedRegion):
     """
     Creates treeview widget "statsTab"  containing all stats of gene,intergene, exon and intron
     """

     if selectedRegion.cget("text") == "Aucune région sélectionnée" or selectedRegion.cget("text") == "" : 
          messagebox.showwarning("Selection de région","Veuillez sélectionner une région")
     else :
          for widget in resultsFrame.winfo_children() :
               widget.destroy()
          
          window.geometry("730x420+350+0")

          graphTitle = ttk.Label(resultsFrame,text="Statistiques (Tailles en acides nucleiques)",foreground="black")
          graphTitle.grid(column=0,row=0,pady=15,columnspan=4)
          

          statsTab = ttk.Treeview(resultsFrame,height=4)

          geneMin,geneMax,geneAllMean=resultFeature("gene")
          exonMin,exonMax,exonAllMean=resultFeature("exon")
          intronMin,intronMax,intronAllMean=resultFeature("intron") 
          intergenesMin,intergenesMax,intergenesAllMean=resultIntergenes()

          
          #Define columns
          statsTab["columns"] = ("Minimum","Maximum","Mean",)

          statsTab.column("#0",anchor=CENTER,width=120,minwidth=120)
          statsTab.column("Minimum",anchor=CENTER,width=120,minwidth=120)
          statsTab.column("Maximum",anchor=CENTER,width=120,minwidth=120)
          statsTab.column("Mean",anchor=CENTER,width=120,minwidth=120)

          statsTab.heading("#0",text="",anchor=CENTER)
          statsTab.heading("Minimum",text="Minimum",anchor=CENTER)
          statsTab.heading("Maximum",text="Maximum",anchor=CENTER)
          statsTab.heading("Mean",text="Moyenne",anchor=CENTER)

          statsTab.insert(parent="",index='end',iid=0,text="Genes",value=(geneMin,geneMax,geneAllMean))
          statsTab.insert(parent="",index='end',iid=1,text="Intergenes",value=(intergenesMin,intergenesMax,intergenesAllMean))
          statsTab.insert(parent="",index='end',iid=2,text="Exons",value=(exonMin,exonMax,exonAllMean))
          statsTab.insert(parent="",index='end',iid=3,text="Introns",value=(intronMin,intronMax,intronAllMean))

          statsTab.grid(column=0,row=1,rowspan=1,columnspan=4)

     return    