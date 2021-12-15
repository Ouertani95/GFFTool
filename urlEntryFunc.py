import tkinter as tk
import wget
import validators
import os
import tkinter.ttk as ttk

def customBar(current,total,width=80):
     """
     Shows download progress while file is downloading
     """
     downloadProgress["value"]=current / total *100
     wrongUrl.config(text=str(round(downloadProgress["value"]))+" % "+"["+str(current)+" / "+str(total)+"]" +" bytes",foreground="black")
     wrongUrl.pack()
     downloadWindow.update_idletasks()
     return

def fileDownload ():
     """
     Once downloadButton is pressed verifies the content of entryField :
     1) If entryField doesn't contain a valid url : shows "Url non valide"
     2) If entryField contains a valid url but no gff file : shows "Pas de fichier gff trouvé"
     3) If entryField contains a valid url and a gff file : Downloads file and shows "Ouvrir le fichier en local"
     """
     urlLink = urlEntry.get()
     validUrl=validators.url(urlLink)
          
     if validUrl!=True :  
          entryField.delete(0,tk.END) #refresh entryField
          wrongUrl.pack_forget() #remove old text from wrongUrl Label
          wrongUrl.config(text="Url non valide")
          wrongUrl.pack(pady=10)
     elif ("gff" not in urlLink) and ("gtf" not in urlLink) :
          entryField.delete(0,tk.END)
          wrongUrl.pack_forget()
          wrongUrl.config(text="Pas de fichier gff trouvé")
          wrongUrl.pack(pady=10)
     else :
          wrongUrl.pack_forget()
          wget.download(url=urlLink,bar=customBar)
          os.system("gzip -d -f *.gz")
          wrongUrl.pack_forget()
          wrongUrl.config(text="Ouvrir le fichier en local",foreground="#dd4814")
          wrongUrl.pack(pady=10)
     return

def urlEntryFunc():
     """
     Creates download window
     """

     global downloadWindow
     downloadWindow = tk.Toplevel()
     downloadWindow.geometry("410x190+670+0")
     downloadWindow.title("GFF Download")
     downloadWindow.configure(bg="#F6F6F5")

    
     entryLabel = tk.Label(downloadWindow,text="Saisir l'url du fichier gff",bg="#F6F6F5")
     entryLabel.pack(pady=10)

     global urlEntry
     urlEntry= tk.StringVar()
     global entryField
     entryField = ttk.Entry(downloadWindow,textvariable=urlEntry,width=35)
     entryField.pack(pady=5)
          
          
     downloadButton = ttk.Button(downloadWindow,text="Télécharger",command=fileDownload)
     downloadButton.pack(pady=5)

     global downloadProgress
     downloadProgress = ttk.Progressbar(downloadWindow,length=300,mode="determinate",orient=tk.HORIZONTAL)
     downloadProgress.pack(pady=5)
          
     global wrongUrl
     wrongUrl = ttk.Label(downloadWindow,text="")
     wrongUrl.pack(pady=5)

     downloadWindow.mainloop()
     
     return