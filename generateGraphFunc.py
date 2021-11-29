import fileSelectFunc as fs
import urlEntryFunc as ue
import regionFunc as rf
import genesExonsFunc as ge
import generateStatFunc as gs
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

def generateGraphFunc ():
     co= sqlite3.connect(fs.dbName)
     c = co.cursor()

     global exonT
     exonT= c.execute("SELECT end-start from features WHERE featuretype = 'exon'").fetchall()
     
     global geneT
     geneT= c.execute("SELECT end-start from features WHERE featuretype = 'gene'").fetchall()
     
     global intronT
     intronT= c.execute("SELECT end-start from features WHERE featuretype ='intron'").fetchall()
     
     plt.plot(exonT,label='exon')
     plt.plot(geneT,label='gene')
     plt.plot(intronT,label='intron')

     plt.xlabel('Nombre')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de la taille')
     plt.legend(ncol=3,loc='upper right')
     #bbox_to_anchor=(0.5,-0.1)
     plt.show()
     co.commit()
     c.close()
     co.close()
     return

