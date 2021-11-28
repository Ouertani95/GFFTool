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
     graphWindow = tk.Tk()
     graphWindow.geometry("500x500+700+100")
     graphWindow.title("GFF Graphs")