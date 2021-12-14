from fileSelectFunc import *
from urlEntryFunc import *
from regionFunc import *
from genesExonsFunc import *
from generateGraphFunc import *
from generateStatFunc import *
from pdfGenerator import *
import tkinter as tk
from tkinter.constants import W
import tkinter.ttk as ttk 
import ttkthemes as themes

def windowGFFTool ():

    window = themes.ThemedTk(theme="radiance")
    window.geometry("730x230+350+0")
    window.title("GFF Tool")
    window.configure(bg="#F6F6F5")


    selectionFrame = tk.Frame(window,background="#F6F6F5")
    selectionFrame.grid(column=0,row=0,padx=5)


    selectLabel = ttk.Label(selectionFrame,text="Sélectionner un fichier .GFF",foreground="black",background="#F6F6F5")
    selectLabel.grid(column=0,row=0,padx=65,pady=10,sticky="W")

    selectLocal = ttk.Button(selectionFrame,text="En local",
    command= lambda : fileSelectFunc(window,selectedFile,resultsFrame,selectedRegion))
    selectLocal.grid(column=0,row=1,padx=90,pady=5,sticky="W")

    selectedFile = ttk.Label(selectionFrame,text="Aucun fichier sélectionné",background="#F6F6F5",foreground="#2E2E2E")
    selectedFile.grid(column=0,row=2,padx=10,pady=5,ipadx=7)

    selectOnline = ttk.Button(selectionFrame,text="En ligne",command=urlEntryFunc)
    selectOnline.grid(column=0,row=3,padx=90,pady=5,sticky="W")

    pdfButton = ttk.Button(selectionFrame,text="Générer pdf", width=15,
    command= lambda : pdfGenerator(window,resultsFrame,selectedRegion))
    pdfButton.grid(column=0,row=4,padx=74,pady=5,sticky="W")



    programFrame = tk.Frame(window,background="#F6F6F5")
    programFrame.grid(column=1,row=0)


    programLabel = ttk.Label(programFrame,text="Sélectionner un outil",foreground="black",background="#F6F6F5")
    programLabel.grid(row=0,padx=120,pady=10,sticky=W)

    genomicRegion = ttk.Radiobutton(programFrame,text="Définir une région génomique",value=1,
    command= lambda : regionFunc(window,selectedRegion,resultsFrame,selectedFile))
    genomicRegion.grid(row=1,padx=50,pady=5,sticky=W)

    selectedRegion = ttk.Label(programFrame,text="Aucune région sélectionnée",background="#F6F6F5",foreground="#2E2E2E")
    selectedRegion.grid(row=2,padx=50,pady=11,sticky=W)

    numberGenes = ttk.Radiobutton(programFrame,text="Nombres de gènes ,exons et introns",value=2,
    command= lambda : genesExonsFunc(window,resultsFrame,selectedRegion)) 
    numberGenes.grid(row=3,padx=50,pady=5,sticky=W)

    graphGenerator = ttk.Radiobutton(programFrame,text="Générer des graphiques",value=3,
    command= lambda : generateGraphFunc(window,resultsFrame,selectedRegion))
    graphGenerator.grid(row=4,padx=50,pady=5,sticky=W)

    statGenerator = ttk.Radiobutton(programFrame,text="Générer des statistiques",value=4,
    command= lambda : generateStatFunc(window,resultsFrame,selectedRegion)) 
    statGenerator.grid(row=5,padx=50,pady=5,sticky=W)


    resultsFrame=tk.Frame(window,background="#F6F6F5",height=450,width=700)
    resultsFrame.grid(column=0,row=1,columnspan=2,pady=10,ipady=10)

    window.mainloop()
    return

if __name__ == "__main__" :
    windowGFFTool()