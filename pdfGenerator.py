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
            print("## Nombres de genes,exons et introns:\n",file=f)

            plusGenes,plusExons,plusIntrons=ge.getPlus()
            minusGenes,minusExons,minusIntrons=ge.getMinus()
            bothGenes,bothExons,bothIntrons=ge.getBoth()

            print("<table border = '1' width = '70%' >\n",file=f)

            print("<thead>\n"+"<tr>\n",file=f)
            print("<th>      </th>\n",file=f)
            print("<th> Genes</th>\n",file=f)
            print("<th> Exons</th>\n",file=f)
            print("<th> Introns</th>\n",file=f)
            print("</tr>\n"+"</thead>\n",file=f)

            print("<tbody>\n"+"<tr>\n",file=f)
            print("<td>Brin +</td>\n",file=f)
            print("<td style='text-align:center'>"+str(plusGenes)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(plusExons)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(plusIntrons)+"</td>\n",file=f)
            print("</tr>\n",file=f)

            print("<tr>\n",file=f)
            print("<td>Brin -</td>\n",file=f)
            print("<td style='text-align:center'>"+str(minusGenes)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(minusExons)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(minusIntrons)+"</td>\n",file=f)
            print("</tr>\n",file=f)

            print("<tr>\n",file=f)
            print("<td>2 Brins</td>\n",file=f)
            print("<td style='text-align:center'>"+str(bothGenes)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(bothExons)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(bothIntrons)+"</td>\n",file=f)
            print("</tr>\n"+"</tbody>\n"+"</table>\n",file=f)

            geneMin,geneMax,geneAllMean=gs.resultGene()
            exonMin,exonMax,exonAllMean=gs.resultExon()
            intronMin,intronMax,intronAllMean=gs.resultIntron() 
            intergenesMin,intergenesMax,intergenesAllMean=gs.resultIntergenes()
            
            print("## Statistiques:\n",file=f)
            
            print("<table border = '1' width = '70%' >\n",file=f)

            print("<thead>\n"+"<tr>\n",file=f)
            print("<th>      </th>\n",file=f)
            print("<th> Minimum</th>\n",file=f)
            print("<th> Maximum</th>\n",file=f)
            print("<th> Moyenne</th>\n",file=f)
            print("</tr>\n"+"</thead>\n",file=f)

            print("<tbody>\n"+"<tr>\n",file=f)
            print("<td>Genes</td>\n",file=f)
            print("<td style='text-align:center'>"+str(geneMin)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(geneMax)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(geneAllMean)+"</td>\n",file=f)
            print("</tr>\n",file=f)

            print("<tr>\n",file=f)
            print("<td>Intergenes</td>\n",file=f)
            print("<td style='text-align:center'>"+str(intergenesMin)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(intergenesMax)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(intergenesAllMean)+"</td>\n",file=f)
            print("</tr>\n",file=f)

            print("<tr>\n",file=f)
            print("<td>Exons</td>\n",file=f)
            print("<td style='text-align:center'>"+str(exonMin)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(exonMax)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(exonAllMean)+"</td>\n",file=f)
            print("</tr>\n",file=f)

            print("<tr>\n",file=f)
            print("<td>Introns</td>\n",file=f)
            print("<td style='text-align:center'>"+str(intronMin)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(intronMax)+"</td>\n",file=f)
            print("<td style='text-align:center'>"+str(intronAllMean)+"</td>\n",file=f)
            print("</tr>\n"+"</tbody>\n"+"</table>\n",file=f)

            print("## Graphes :\n",file=f)
            
            gg.generateGraphGene(0,1)
            print("![image caption](/home/ouertani/Desktop/projetProgrammation2021/Figures/barGene.png)",file=f)
            gg.generateGraphInter(0,1)
            print("![image caption](/home/ouertani/Desktop/projetProgrammation2021/Figures/barInter.png)",file=f)
            gg.generatePiechartGenesIntergeniques(0,1)
            print("![image caption](/home/ouertani/Desktop/projetProgrammation2021/Figures/pieGeneInter.png)",file=f)
            gg.generateBoxplot1(0,1)
            print("![image caption](/home/ouertani/Desktop/projetProgrammation2021/Figures/box1.png)",file=f)
            gg.generateGraphExon(0,1)
            print("![image caption](/home/ouertani/Desktop/projetProgrammation2021/Figures/barExon.png)",file=f)
            gg.generateGraphIntron(0,1)
            print("![image caption](/home/ouertani/Desktop/projetProgrammation2021/Figures/barIntron.png)",file=f)
            gg.generatePiechartExonsIntrons(0,1)
            print("![image caption](/home/ouertani/Desktop/projetProgrammation2021/Figures/pieExonsIntrons.png)",file=f)
            gg.generateBoxplot2(0,1)
            print("![image caption](/home/ouertani/Desktop/projetProgrammation2021/Figures/box2.png)",file=f)
            
        os.system("markdown "+mdFileName+".md"+" > "+mdFileName+".html")
        pdfkit.from_file(mdFileName+'.html', mdFileName+'.pdf')
        
        path = mdFileName+'.pdf'
        webbrowser.open_new(path)

        os.system("rm ./Figures/*.md ./Figures/*.html")
    
    return