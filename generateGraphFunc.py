import fileSelectFunc as fs
import regionFunc as rf
from tkinter.constants import W
import numpy as np 
import matplotlib.pyplot as plt 
import sqlite3
import pandas as pd
import tkinter.ttk as ttk 
from tkinter import messagebox
import matplotlib as mpl
from matplotlib import pylab
import seaborn as sns


def calculFeature(feature) :
     """
     Calculates the position and length of each feature and retrieves the sum of all the features present in the chromosome
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     featureT= cur.execute("SELECT end-start from features WHERE featuretype = '%s' and seqid='%s' and start >=%s and end<=%s"%(feature,rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

     featureTInt = []
     for featureLength in featureT :
          featureTInt.append(featureLength[0])

     featurePositions = [*range(1,len(featureT)+1)]

     sumFeatures = 0
     for g in featureTInt :
          sumFeatures+= g

     con.commit()
     cur.close()
     con.close()
     return featureTInt,featurePositions,sumFeatures

def calculIntergenes() :
     """
     Calculates the position and length of each intergenes and retrieves the sum of all the intergenes present in the chromosome
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     startGenePlus = cur.execute("SELECT start from features WHERE featuretype ='gene' and strand = '+' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

     endGenePlus= cur.execute("SELECT end from features WHERE featuretype ='gene' and strand = '+' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          
     interArrayPlus = np.column_stack((startGenePlus,endGenePlus))

     #determines the length of intergenes from start and end positions of genes
     interListPlus = []
     for inter in range (1,len(interArrayPlus)) :
          if interArrayPlus[inter,0] - interArrayPlus[inter-1,1] < 0 :
               continue
          else :
               interListPlus.append(interArrayPlus[inter,0] - interArrayPlus[inter-1,1])


     startGeneMinus= cur.execute("SELECT start from features WHERE featuretype ='gene' and strand = '-' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

     endGeneMinus= cur.execute("SELECT end from features WHERE featuretype ='gene' and strand = '-' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

     interArrayMinus = np.column_stack((startGeneMinus,endGeneMinus))

     interListMinus = []
     for inter in range (1,len(interArrayMinus)) :
          if interArrayMinus[inter,0] - interArrayMinus[inter-1,1] < 0 :
               continue
          else : 
               interListMinus.append(interArrayMinus[inter,0] - interArrayMinus[inter-1,1])

     interListBoth = interListPlus + interListMinus 

     sumInter = 0
     for v in interListBoth :
          sumInter+= v
 
     interPositionsBoth = [*range(1,len(interListBoth)+1)]


     con.commit()
     cur.close()
     con.close()
     return interListBoth,sumInter,interPositionsBoth


def generateGraphGene(show,save):
     """
     Generates a barplot representing the distribution of gene sizes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     geneTInt,genePositions,sumGenes=calculFeature("gene")
     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig2 = pylab.gcf()
     fig2.canvas.manager.set_window_title('Graphes des genes')
     plt.bar(genePositions,geneTInt,label='Gene',color='olive')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de taille des genes sur les 2 brins',fontsize=13)
     plt.legend(ncol=3,loc='upper right')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./barGene.png")
          plt.close()
     return


def generateGraphInter(show,save): 
     """
     Generates a barplot representing the distribution of intergene sizes inside the chromosome region
     """ 

     plt.figure(figsize=(7, 5))
     interListBoth,sumInter,interPositionsBoth=calculIntergenes()
     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig1 = pylab.gcf()
     fig1.canvas.manager.set_window_title('Graphes des régions intergéniques')
     plt.bar(interPositionsBoth,interListBoth,label='Régions Intergéniques',color='yellowgreen')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de taille des régions intergéniques sur les 2 brins',fontsize=11)
     plt.legend(ncol=4,loc='upper right')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./barInter.png")
          plt.close()
     return

def generateGraphExon (show,save):
     """
     Generates a barplot representing the distribution of exon sizes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     exonTInt,exonPositions,sumExons=calculFeature("exon")
     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig1 = pylab.gcf()
     fig1.canvas.manager.set_window_title('Graphes des exons')
     plt.bar(exonPositions,exonTInt,label='exon',color='darksalmon')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de taille des exons sur les 2 brins',fontsize=13)
     plt.legend(ncol=3,loc='upper right')
          
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./barExon.png")
          plt.close()
     return

def generateGraphIntron(show,save):
     """
     Generates a barplot representing the distribution of intron sizes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     intronTInt,intronPositions,sumIntrons=calculFeature("intron")
     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig3 = pylab.gcf()
     fig3.canvas.manager.set_window_title('Graphes des introns')
     plt.bar(intronPositions,intronTInt,label='Intron',color='firebrick')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de taille des introns sur les 2 brins',fontsize=13)
     plt.legend(ncol=3,loc='upper right')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./barIntron.png")
          plt.close()
     return

def generatePiechartGenesIntergenes (show,save):
     """
     Generates a piechart representing the size percentages of genes and intergenes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     geneTInt,genePositions,sumGenes=calculFeature("gene")
     interListBoth,sumInter,interPositionsBoth=calculIntergenes()
     values1 = [sumGenes,sumInter]
     Names1 = ["Genes","Intergenes"]
     col=['olive','yellowgreen']
     figP = pylab.gcf()
     figP.canvas.manager.set_window_title('Distributions des genes et des intergenes')
     plt.pie(values1,labels=Names1,autopct="%.1f%%",wedgeprops={'edgecolor':'white', 'linewidth':2},colors=col)
     plt.title('Pourcentages des genes et intergenes')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./pieGeneInter.png")
          plt.close()
     return

def generatePiechartExonsIntrons (show,save):
     """
     Generates a piechart representing the size percentages of exons and introns inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     intronTInt,intronPositions,sumIntrons=calculFeature("intron")
     exonTInt,exonPositions,sumExons=calculFeature("exon")
     values = [sumIntrons,sumExons]
     Names = ["Introns","Exons"]
     col=['firebrick','darksalmon']
     figP = pylab.gcf()
     figP.canvas.manager.set_window_title('Distributions des exons et des intron')
     plt.pie(values,labels=Names,autopct="%.1f%%",wedgeprops={'edgecolor':'white', 'linewidth':2},colors=col)
     plt.title('Pourcentages des exons et introns')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./pieExonsIntrons.png")
          plt.close()
     return

def generateBoxplot1(show,save) :
     """
     Generates a boxplot comparing the size distribution of genes and intergenes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     geneTInt,genePositions,sumGenes=calculFeature("gene")
     interListBoth,sumInter,interPositionsBoth=calculIntergenes()
     figB1 = pylab.gcf()
     figB1.canvas.manager.set_window_title('Boxplot des genes et des intergenes')
     a = pd.DataFrame({ '' : np.repeat('Genes',len(geneTInt)), 'Taille (acide nucleique)': geneTInt })
     b = pd.DataFrame({ '' : np.repeat('Intergenes',len(interListBoth)), 'Taille (acide nucleique)': interListBoth })
     df=a.append(b)
     my_pal2 = {"Genes": "olive", "Intergenes": "yellowgreen"}
     sns.boxplot(x='', y='Taille (acide nucleique)', data=df,showmeans=True,palette=my_pal2)
     plt.title('Comparaison de taille entre genes et intergenes')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./box1.png")
          plt.close()
     return 


def generateBoxplot2(show,save) :
     """
     Generates a boxplot comparing the size distribution of exons and introns inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     exonTInt,exonPositions,sumExons=calculFeature("exon")
     intronTInt,intronPositions,sumIntrons=calculFeature("intron")
     figB2 = pylab.gcf()
     figB2.canvas.manager.set_window_title('Boxplot des exons et des introns')
     c = pd.DataFrame({ '' : np.repeat('Exons',len(exonTInt)), 'Taille (acide nucleique)': exonTInt })
     d = pd.DataFrame({ '' : np.repeat('Introns',len(intronTInt)), 'Taille (acide nucleique)':intronTInt })
     df=c.append(d)
     my_pal1 = {"Exons": "darksalmon", "Introns": "firebrick"}
     sns.boxplot(x='', y='Taille (acide nucleique)', data=df,showmeans=True,palette=my_pal1)
     plt.title('Comparaison de taille entre exons et introns')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./box2.png")
          plt.close()
     return

def generateGraphFunc (window,resultsFrame,selectedRegion):
     """
     Creates the graph interface inside the resultsFrame with all graph buttons
     """

     if selectedRegion.cget("text") == "Aucune région sélectionnée" or selectedRegion.cget("text") == "" : 
          messagebox.showwarning("Selection de région","Veuillez sélectionner une région")
     else :
          for widget in resultsFrame.winfo_children() :
               widget.destroy()
          
          window.geometry("730x550+350+0")

          mainTitle = ttk.Label(resultsFrame,text="Generation des graphes",foreground="black")
          mainTitle.grid(column=0,row=0,pady=15,columnspan=3)

          barTitle = ttk.Label(resultsFrame,text="Distributions des tailles",foreground="black")
          barTitle.grid(column=0,row=1,padx=20,pady=5)

          pieTitle = ttk.Label(resultsFrame,text="Proportions",foreground="black")
          pieTitle.grid(column=1,row=1,padx=20,pady=5)

          boxTitle = ttk.Label(resultsFrame,text="Comparaison des distributions",foreground="black")
          boxTitle.grid(column=2,row=1,padx=20,pady=5)


          gene_Button = ttk.Button(resultsFrame,text="Genes",command= lambda  : generateGraphGene(1,0))
          gene_Button.grid(column=0,row=2,pady=10,padx=25)

          inter_Button = ttk.Button(resultsFrame,text="Intergenes",command= lambda : generateGraphInter(1,0))
          inter_Button.grid(column=0,row=3,pady=10,padx=25)

          exon_Button = ttk.Button(resultsFrame,text="Exons",command= lambda : generateGraphExon(1,0))
          exon_Button.grid(column=0,row=4,pady=10,padx=25)

          intron_Button = ttk.Button(resultsFrame,text="Introns",command= lambda : generateGraphIntron(1,0))
          intron_Button.grid(column=0,row=5,pady=10,padx=25)

          pie2_Button = ttk.Radiobutton(resultsFrame,text='Genes/Intergenes',command= lambda : generatePiechartGenesIntergenes(1,0))
          pie2_Button.grid(column=1,row=2,padx=30,ipady= 25,sticky=W,rowspan=2) 

          pie1_Button = ttk.Radiobutton(resultsFrame,text='Exons/Introns',command= lambda :generatePiechartExonsIntrons(1,0))
          pie1_Button.grid(column=1,row=4,padx=30,ipady= 25,sticky=W,rowspan=2) 

          box1_Button = ttk.Button(resultsFrame,text='Boxplot G/I',command= lambda : generateBoxplot1(1,0))
          box1_Button.grid(column=2,row=2,padx=20,pady=5,rowspan=2)

          box2_Button = ttk.Button(resultsFrame,text='Boxplot E/I',command=lambda : generateBoxplot2(1,0))
          box2_Button.grid(column=2,row=4,padx=20,pady=5,rowspan=2)
     return