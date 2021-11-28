from re import A
import tkinter as tk
from tkinter import StringVar, filedialog
from tkinter.constants import ANCHOR, E, LEFT, NS, NSEW, RAISED, RIGHT, VERTICAL, W, Y
import wget
import validators
from glob import glob
import os
import numpy as np 
import matplotlib.pyplot as plt
import  gffutils
from gffutils.create import create_db
from pathlib import Path
import sqlite3
import pandas as pd 



def fileSelect() :
     #Afficher la fenêtre de selection du fichier gff en local
     window.filename = filedialog.askopenfilename(initialdir="~/Desktop/Projet_programmation/test_db",title="Selectionner un fichier gff",filetypes=(("gff files","*.gff"),("gff3 files",".gff3"),("gtf files","*.gtf"),("all files","*.*")))
     #extraire nom de fichier sans extension  à partir du fichier séléctionner en local 
     nameFile = Path(window.filename).stem
     print(nameFile)
     #créer nom de la base de données 
     global dbName
     dbName = nameFile + ".db"
     print(dbName)

     if os.path.exists(dbName)==False :
     #créer la base de données 
          db = gffutils.create_db(window.filename, dbName)
          db = gffutils.FeatureDB(dbName)
     
     #se connecter à la base de données 
     con = sqlite3.connect(dbName)
     cur = con.cursor()
     #créer les listes de chromosomes, start et end à partir de la base de données créée
     global chrID
     chrID = cur.execute("SELECT DISTINCT seqid FROM features").fetchall()
     
     # check intrus chromosomes
     # chrID2 = cur.execute("SELECT DISTINCT seqid FROM features").fetchall()
     # chrID3 = []
     # for chr in chrID2 :
     #      if chr not in chrID :
     #           chrID3 += chr   
     
     # print (chrID3)
     print(chrID)
     print(type(chrID))
     print("le nombre de chromosomes est : ",len(chrID))
     # if len(chrID) == 1 :
     global startList
     startList = cur.execute("SELECT DISTINCT start FROM features ORDER BY start asc").fetchall()
     # print("La liste des positions start est :",startList)
     # print(type(startList))
     global endList
     endList = cur.execute("SELECT DISTINCT end FROM features ORDER BY end desc").fetchall()
     # print("La liste des positions end est :",endList)
     # print(type(endList))
     # else :
     #           chrSelection = region().get("anchor")
     #           print(chrSelection)
     #      # startList = cur.execute("SELECT DISTINCT start FROM features WHERE seqid = %s"%chrSelection).fetchall()
     #      # endList = cur.execute("SELECT DISTINCT end FROM features WHERE seqid = %s"%chrSelection).fetchall()
     con.commit()
     cur.close()
     con.close()

def urlEntry():
     urlEntry= tk.StringVar()
     entryLabel = tk.Label(window,text="Saisir l'url du fichier gff")
     entryLabel.grid(column=0,row=5)
     entryField = tk.Entry(window,textvariable=urlEntry)
     entryField.grid(column=0,row=6)

     def fileDownload ():
          urlLink = urlEntry.get()
          validUrl=validators.url(urlLink)
          print(validUrl)
          wrongUrl = tk.Label(window,text="")
          if validUrl!=True :
               entryField.delete(0,tk.END)
               wrongUrl = tk.Label(window,text="").grid(column=0,row=6)
               wrongUrl = tk.Label(window,text="Url non valide")
               wrongUrl.grid(column=0,row=8)
          elif "gff" not in urlLink :
               entryField.delete(0,tk.END)
               wrongUrl = tk.Label(window,text="").grid(column=0,row=6)
               wrongUrl = tk.Label(window,text="Pas de fichier gff trouvé")
               wrongUrl.grid(column=0,row=8)
          else :
               print(urlLink)
               wget.download(url=urlLink)
               path = '~/Desktop/Projet_programmation/test_db/' # Show location of the files
               list_of_files = glob(path + '*.gz') # list gzip files
               bash_command = 'gzip -dk -f ' + ' '.join(list_of_files) # create bash command
               os.system(bash_command) # Run command in Terminal
               wrongUrl = tk.Label(window,text="Ficher téléchargé et dézippé veuillez ouvrir en local")
               wrongUrl.grid(column=0,row=8)
               #shutil.unpack_archive("dmel-2RHet-r5.54.gff.gz")
               #gzip.decompress()
     
     downloadButton = tk.Button(window,text="Telecharger",command=fileDownload)
     downloadButton.grid(column=0,row=7)  

def region():
     regionWindow = tk.Tk()
     regionWindow.geometry("650x350+700+100")
     regionWindow.title("GFF Region")

     chrScrollbar = tk.Scrollbar(regionWindow,orient=VERTICAL)
     startScrollbar = tk.Scrollbar(regionWindow,orient=VERTICAL)
     endScrollbar = tk.Scrollbar(regionWindow,orient=VERTICAL)

     chrLabel = tk.Label(regionWindow,text="Chromosome")
     chrLabel.grid (column=0,row=0,padx=20,pady=10)
     startLabel = tk.Label(regionWindow,text="Start")
     startLabel.grid (column=1,row=0,padx=20,pady=10)
     endLabel = tk.Label(regionWindow,text="End")
     endLabel.grid (column=2,row=0,padx=20,pady=10)

     global chrChoice
     chrChoice = tk.Listbox(regionWindow,yscrollcommand=chrScrollbar.set,exportselection=0)
     chrChoice.grid(column=0,row=1,padx=20,pady=10)
     
     for chromosome in chrID :
          chrChoice.insert("end",chromosome)
     chrScrollbar.config(command=chrChoice.yview)
     chrScrollbar.grid(column=0,row=1,sticky='e''n''s')
     selectChr = chrChoice.get("anchor")
     print("le chromosome séléctionné est ",str(selectChr))
     def confirmerChoix():
          confChr = chrChoice.get(ANCHOR)
          return confChr
     confirmChr = tk.Button(regionWindow,text="Confirmer choix",command=confirmerChoix)

     #if selectChr != "" :

     startChoice = tk.Listbox(regionWindow,yscrollcommand=startScrollbar.set,exportselection=0)
     startChoice.grid(column=1,row=1,padx=20,pady=10)
     for start in startList :
          startChoice.insert("end",start)
     startScrollbar.config(command=startChoice.yview)
     startScrollbar.grid(column=1,row=1,sticky='e''n''s')

     endChoice = tk.Listbox(regionWindow,yscrollcommand=endScrollbar.set,exportselection=0)
     endChoice.grid(column=2,row=1,padx=20,pady=10)
     for end in endList :
          endChoice.insert("end",end)
     endScrollbar.config(command=endChoice.yview)
     endScrollbar.grid(column=2,row=1,sticky='e''n''s')

     def save ():
          global chrSelected
          chrSelected = "".join(chrChoice.get("anchor"))
          print(chrSelected)
          print(type(chrSelected))
          startTuple = startChoice.get("anchor")
          global startSelected
          startSelected = startTuple[0]
          print(startSelected)
          print(type(startSelected))
          endTuple = endChoice.get("anchor")
          global endSelected
          endSelected = endTuple[0]
          print(endSelected)
          print(type(endSelected))

          return

     SaveButton = tk.Button(regionWindow,text="Sauvegarder",command=save)
     SaveButton.grid(column=1,row=3,pady=10)
     regionQuitButton = tk.Button(regionWindow,text="Quitter",command=regionWindow.destroy)
     regionQuitButton.grid(column=1,row=4,pady=10)

     return chrChoice


def genes_exons():
     #Anchor
     nbrWindow = tk.Tk()
     nbrWindow.geometry("400x100+700+100")
     nbrWindow.title("Region numbers")
     
     con = sqlite3.connect(dbName)
     cur = con.cursor()

     numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='CDS' and start>=%s and end <=%s"%(startSelected,endSelected)).fetchall()
     numberGenes = numberGenesList[0][0]
     print(numberGenes)
     print(type(numberGenes))

     geneResult = tk.Label(nbrWindow,text="Le nombre de gènes dans cette région est : "+str(numberGenes))
     geneResult.grid(row=0,pady=10)

     numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and start>=%s and end <=%s"%(startSelected,endSelected)).fetchall()
     numberExons = numberExonsList[0][0]
     print(numberExons)
     print(type(numberExons))

     exonResult = tk.Label(nbrWindow,text="Le nombre d'exons dans cette région est : "+str(numberExons))
     exonResult.grid(row=1,pady=10)

     con.commit()
     cur.close()
     con.close()

def generateGraph ():
     graphWindow = tk.Tk()
     graphWindow.geometry("500x500+700+100")
     graphWindow.title("GFF Graphs")
     return

def generateStat ():
     statWindow = tk.Tk()
     statWindow.geometry("500x500+700+100")
     statWindow.title("GFF Stats")
     return

window = tk.Tk()
window.geometry("500x250")
window.title("GFF Tool")
#window.configure(bg="grey")

programFrame = tk.Frame(window)
programFrame.grid(column=1,row=0,rowspan=20)


programLabel = tk.Label(programFrame,text="Selectionner un outil")
programLabel.grid(row=0,padx=50)
genomicRegion = tk.Radiobutton(programFrame,text="Définir une région génomique",value=1,command=region)
genomicRegion.grid(row=1)
numberGenes = tk.Radiobutton(programFrame,text="Récupérer nombre de gènes et exons",value=2,command=genes_exons) 
numberGenes.grid(row=2)
graphGenerator = tk.Radiobutton(programFrame,text="Générer des graphiques",value=3,command=generateGraph)
graphGenerator.grid(row=3)
statGenerator = tk.Radiobutton(programFrame,text="Générer des statistiques",value=4,command=generateStat) 
statGenerator.grid(row=4)


selectLabel = tk.Label(window,text="Selectionner un fichier .GFF")
selectLabel.grid(column=0,row=0,pady=5)
selectLocal = tk.Button(window,text="En local",command=fileSelect)
selectLocal.grid(column=0,row=1,pady=5)
selectOnline = tk.Button(window,text="En ligne",command=urlEntry)
selectOnline.grid(column=0,row=2,pady=5)


quitButton = tk.Button(window,text="Quitter", bg="sky blue", width=15, command=window.destroy)
quitButton.grid(column=0,row=10,pady=5)


window.mainloop()