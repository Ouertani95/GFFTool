import fileSelectFunc as fs
import urlEntryFunc as ue
import regionFunc as rf
import genesExonsFunc as ge
import generateGraphFunc as gg
import generateStatFunc as gs
from tkinter import messagebox
import matplotlib.pyplot as plt
import os
import pdfkit
import webbrowser

def pdfGenerator (window,resultsFrame,selectedRegion) : 
    if selectedRegion.cget("text") == "Aucune région sélectionnée" or selectedRegion.cget("text") == "" : 
          messagebox.showwarning("Selection de région","Veuillez sélectionner une région")
    else :

        mdFileName="./Figures/"+fs.nameFile+"_"+selectedRegion.cget("text")
        with open(mdFileName+".md","w") as f :

            gg.generateGraphFunc(window,resultsFrame,selectedRegion)
            print("# Fichier : "+fs.nameFile,file=f)
            print("## Region : "+selectedRegion.cget("text"),file=f)
            print("## Nombres de genes,exons et introns: ",file=f)

            plusGenes,plusExons,plusIntrons=ge.getPlus()
            print("## Brin(+) :",file=f)
            print("Genes : "+str(plusGenes)+'\n',file=f)
            print("Exons : "+str(plusExons)+'\n',file=f)
            print("Introns : "+str(plusIntrons)+'\n',file=f)

            minusGenes,minusExons,minusIntrons=ge.getMinus()
            print("## Brin(-) :",file=f)
            print("Genes : "+str(minusGenes)+'\n',file=f)
            print("Exons : "+str(minusExons)+'\n',file=f)
            print("Introns : "+str(minusIntrons)+'\n',file=f)

            bothGenes,bothExons,bothIntrons=ge.getBoth()
            print("## Les 2 brins :",file=f)
            print("Genes : "+str(bothGenes)+'\n',file=f)
            print("Exons : "+str(bothExons)+'\n',file=f)
            print("Introns : "+str(bothIntrons)+'\n',file=f)

            geneMin,geneMax,geneAllMean=gs.resultGene()
            exonMin,exonMax,exonAllMean=gs.resultExon()
            intronMin,intronMax,intronAllMean=gs.resultIntron() 
            intergenesMin,intergenesMax,intergenesAllMean=gs.resultIntergenes()
            print("## Statistiques: ",file=f)

            print("## Minimum :",file=f)
            print("Genes : "+str(geneMin)+'\n',file=f)
            print("Exons : "+str(exonMin)+'\n',file=f)
            print("Introns : "+str(intronMin)+'\n',file=f)
            print("Intergenes : "+str(intergenesMin)+'\n',file=f)

            print("## Maximum :",file=f)
            print("Genes : "+str(geneMax)+'\n',file=f)
            print("Exons : "+str(exonMax)+'\n',file=f)
            print("Introns : "+str(intronMax)+'\n',file=f)
            print("Intergenes : "+str(intergenesMax)+'\n',file=f)

            print("## Moyenne :",file=f)
            print("Genes : "+str(geneAllMean)+'\n',file=f)
            print("Exons : "+str(exonAllMean)+'\n',file=f)
            print("Introns : "+str(intronAllMean)+'\n',file=f)
            print("Intergenes : "+str(intergenesAllMean)+'\n',file=f)

            gg.generateGraphGene(0,1)
            print("![image caption](/home/samerkh/Desktop/projetProgrammation2021/Figures/barGene.png)",file=f)
            gg.generateGraphInter(0,1)
            print("![image caption](/home/samerkh/Desktop/projetProgrammation2021/Figures/barInter.png)",file=f)
            gg.generatePiechartGenesIntergeniques(0,1)
            print("![image caption](/home/samerkh/Desktop/projetProgrammation2021/Figures/pieGeneInter.png)",file=f)
            gg.generateBoxplot1(0,1)
            print("![image caption](/home/samerkh/Desktop/projetProgrammation2021/Figures/box1.png)",file=f)
            gg.generateGraphExon(0,1)
            print("![image caption](/home/samerkh/Desktop/projetProgrammation2021/Figures/barExon.png)",file=f)
            gg.generateGraphIntron(0,1)
            print("![image caption](/home/samerkh/Desktop/projetProgrammation2021/Figures/barIntron.png)",file=f)
            gg.generatePiechartExonsIntrons(0,1)
            print("![image caption](/home//Desktop/projetProgrammation2021/Figures/pieExonsIntrons.png)",file=f)
            gg.generateBoxplot2(0,1)
            print("![image caption](/home/samerkh/Desktop/projetProgrammation2021/Figures/box2.png)",file=f)
            
        os.system("markdown "+mdFileName+".md"+" > "+mdFileName+".html")
        pdfkit.from_file(mdFileName+'.html', mdFileName+'.pdf')
        
        path = mdFileName+'.pdf'
        webbrowser.open_new(path)

        os.system("rm ./Figures/*.md ./Figures/*.html")
        
            
            
            
            




        # my_pdf= FPDF()
        # my_pdf.add_page()
        # my_pdf.set_font("Arial",size=14)
        # my_pdf.cell(10,txt="Résumé de la région : "+selectedRegion.cget("text"),ln=1,align="C")
        # my_pdf.output(fs.nameFile+" : "+selectedRegion.cget("text"))