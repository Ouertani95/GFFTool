import fileSelectFunc as fs
import genesExonsFunc as ge
import generateGraphFunc as gg
import generateStatFunc as gs
from tkinter import messagebox
import os
import pdfkit
import webbrowser

def pdfGenerator (window,resultsFrame,selectedRegion) : 
    if selectedRegion.cget("text") == "Aucune région sélectionnée" or selectedRegion.cget("text") == "" : 
          messagebox.showwarning("Selection de région","Veuillez sélectionner une région")
    else :

        mdFileName="./"+fs.nameFile+"_"+selectedRegion.cget("text")
        with open(mdFileName+".md","w") as f :

            print("<center><h1>Fichier : "+fs.nameFile+"</h1></center><br /><br />",file=f)

            print("<h2>Region : "+selectedRegion.cget("text")+"</h2><br />",file=f)

            print("<h2>Nombres de genes,exons et introns :</h2><br />",file=f)

            plusGenes,plusExons,plusIntrons=ge.getPlus()
            minusGenes,minusExons,minusIntrons=ge.getMinus()
            bothGenes,bothExons,bothIntrons=ge.getBoth()

            print("<center><table border = '2' width = '70%' style='border-style: solid ; border-color: #000000'>\n",file=f)

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
            print("</tr>\n"+"</tbody>\n"+"</table>\n</center>",file=f)


            print("<h2>Statistiques (Tailles en acides nucleiques) :</h2><br />",file=f)

            geneMin,geneMax,geneAllMean=gs.resultGene()
            exonMin,exonMax,exonAllMean=gs.resultExon()
            intronMin,intronMax,intronAllMean=gs.resultIntron() 
            intergenesMin,intergenesMax,intergenesAllMean=gs.resultIntergenes()
            
            print("<center><table border = '2' width = '70%' style='border-style: solid ; border-color: #000000'>\n",file=f)

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
            print("</tr>\n"+"</tbody>\n"+"</table>\n</center>",file=f)

            print("<h2>Graphes :</h2><br />",file=f)

            gg.generateGraphGene(0,1)
            gg.generateGraphInter(0,1)
            gg.generatePiechartGenesIntergenes(0,1)
            gg.generateBoxplot1(0,1)
            gg.generateGraphExon(0,1)
            gg.generateGraphIntron(0,1)
            gg.generatePiechartExonsIntrons(0,1)
            gg.generateBoxplot2(0,1)

            graphs=["barGene","barInter","pieGeneInter","box1","barExon","barIntron","pieExonsIntrons","box2"]
            for graph in graphs : 
                print("<center><img style='border: solid' src='./"+graph+".png'> </center> <br /><br /><br />",file=f)

            
            
        os.system("markdown "+mdFileName+".md"+" > "+mdFileName+".html")
        pdfkit.from_file(mdFileName+'.html', mdFileName+'.pdf')
        
        path = mdFileName+'.pdf'
        webbrowser.open_new(path)

        os.system("rm ./*.md ./*.html ./*.png")
    
    return