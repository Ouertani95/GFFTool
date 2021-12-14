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


def calculGenes() :
     """
     Calculates the position and length of each gene and retrieves the sum of all the genes present in the chromosome
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     geneT= cur.execute("SELECT end-start from features WHERE featuretype = 'gene' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

     geneTInt = []
     for geneLength in geneT :
          geneTInt.append(geneLength[0])

     genePositions = []
     for position in range(1,len(geneT)+1): 
          genePositions.append(position)

     sumGenes = 0
     for g in geneTInt :
          sumGenes+= g

     con.commit()
     cur.close()
     con.close()
     return geneTInt,genePositions,sumGenes

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
 
     interPositionsBoth = []
     for i in range(1,len(interListBoth)+1) : 
          interPositionsBoth.append(i)


     con.commit()
     cur.close()
     con.close()
     return interListBoth,sumInter,interPositionsBoth

def calculExons() :
     """
     Calculates the position and length of each exon and retrieves the sum of all the exons present in the chromosome
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     exonT= cur.execute("SELECT end-start from features WHERE featuretype = 'exon' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          
     exonTInt = []
     for exonLength in exonT :
          exonTInt.append(exonLength[0])

     exonPositions = []
     for position in range(1,len(exonT)+1): 
          exonPositions.append(position)

     sumExons = 0
     for e in exonTInt :
          sumExons += e

     con.commit()
     cur.close()
     con.close()     
     return exonTInt,exonPositions,sumExons 

def calculIntrons() :
     """
     Calculates the position and length of each intron and retrieves the sum of all the introns present in the chromosome
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     intronT= cur.execute("SELECT end-start from features WHERE featuretype ='intron' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

     intronTInt = []
     for intronLength in intronT :
          intronTInt.append(intronLength[0])
          
     intronPositions = []
     for position in range(1,len(intronT)+1): 
          intronPositions.append(position)

     sumIntrons = 0
     for s in intronTInt :
          sumIntrons += s 

     con.commit()
     cur.close()
     con.close() 
     return intronTInt,intronPositions,sumIntrons


def generateGraphGene(show,save):
     """
     Generates a barplot representing the distribution of gene sizes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     geneTInt,genePositions,sumGenes=calculGenes()
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
          plt.savefig("./Figures/barGene.png")
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
          plt.savefig("./Figures/barInter.png")
          plt.close()
     return

def generateGraphExon (show,save):
     """
     Generates a barplot representing the distribution of exon sizes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     exonTInt,exonPositions,sumExons=calculExons()
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
          plt.savefig("./Figures/barExon.png")
          plt.close()
     return

def generateGraphIntron(show,save):
     """
     Generates a barplot representing the distribution of intron sizes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     intronTInt,intronPositions,sumIntrons=calculIntrons()
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
          plt.savefig("./Figures/barIntron.png")
          plt.close()
     return

def generatePiechartGenesIntergeniques (show,save):
     """
     Generates a piechart representing the size percentages of genes and intergenes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     geneTInt,genePositions,sumGenes=calculGenes()
     interListBoth,sumInter,interPositionsBoth=calculIntergenes()
     values1 = [sumGenes,sumInter]
     Names1 = ["Genes","Intergeniques"]
     col=['olive','yellowgreen']
     figP = pylab.gcf()
     figP.canvas.manager.set_window_title('Distributions des genes et des intergenes')
     plt.pie(values1,labels=Names1,autopct="%.1f%%",wedgeprops={'edgecolor':'white', 'linewidth':2},colors=col)
     plt.title('Pourcentage des genes et intergenes')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./Figures/pieGeneInter.png")
          plt.close()
     return

def generatePiechartExonsIntrons (show,save):
     """
     Generates a piechart representing the size percentages of exons and introns inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     intronTInt,intronPositions,sumIntrons=calculIntrons()
     exonTInt,exonPositions,sumExons=calculExons()
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
          plt.savefig("./Figures/pieExonsIntrons.png")
          plt.close()
     return

def generateBoxplot1(show,save) :
     """
     Generates a boxplot comparing the size distribution of genes and intergenes inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     geneTInt,genePositions,sumGenes=calculGenes()
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
          plt.savefig("./Figures/box1.png")
          plt.close()
     return 


def generateBoxplot2(show,save) :
     """
     Generates a boxplot comparing the size distribution of exons and introns inside the chromosome region
     """

     plt.figure(figsize=(7, 5))
     exonTInt,exonPositions,sumExons=calculExons()
     intronTInt,intronPositions,sumIntrons=calculIntrons()
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
          plt.savefig("./Figures/box2.png")
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

          barTitle = ttk.Label(resultsFrame,text="Distribution des tailles",foreground="black")
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

          pie2_Button = ttk.Radiobutton(resultsFrame,text='Genes/Intergenes',command= lambda : generatePiechartGenesIntergeniques(1,0))
          pie2_Button.grid(column=1,row=2,padx=30,ipady= 25,sticky=W,rowspan=2) 

          pie1_Button = ttk.Radiobutton(resultsFrame,text='Exons/Introns',command= lambda :generatePiechartExonsIntrons(1,0))
          pie1_Button.grid(column=1,row=4,padx=30,ipady= 25,sticky=W,rowspan=2) 

          box1_Button = ttk.Button(resultsFrame,text='Boxplot G/I',command= lambda : generateBoxplot1(1,0))
          box1_Button.grid(column=2,row=2,padx=20,pady=5,rowspan=2)

          box2_Button = ttk.Button(resultsFrame,text='Boxplot E/I',command=lambda : generateBoxplot2(1,0))
          box2_Button.grid(column=2,row=4,padx=20,pady=5,rowspan=2)
     return