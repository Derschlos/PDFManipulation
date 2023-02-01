# -*- coding: utf-8 -*-

# venv = r""


import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk
from tkinter.messagebox import showwarning
import os
import math
from PIL import Image, ImageEnhance
import fitz
from multiprocessing import Pool, freeze_support

class WorkPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.pageName = 'WorkPage'
        self.bg = 'lightsalmon'
        self.config(bg = self.bg,)
        self.controller = controller

    
    # Grid
      # Status Frame
        self.statusFrame = tk.Frame(self,bg = self.bg)
        self.progressbar = ttk.Progressbar(self.statusFrame,
                                 orient='horizontal',
                                 mode='determinate',
                                 maximum = 10)
        self.progressLab = tk.Label(self.statusFrame,
                                    text = "",
                                    width = 20,
                                    anchor = 'w',
                                    bg = self.bg)

     # Status grid
        self.statusFrame.grid_columnconfigure(1, weight = 3)
        self.statusFrame.grid(column  = 1, row = 3,
                              padx = 5, pady = 10,
                              columnspan = 2, 
                              sticky = ('e','n','w'))
        self.progressbar.grid(column  = 1, row = 1,
                           sticky= ('e','w'),
                           padx = 3)
        self.progressLab.grid(column  = 2, row = 1)



    def onRaise(self):
        self.controller.root.title('Work Page')

    # Main creation Logic
    def minify(self):
        self.updateProgress('Neue Datei', 0)       
        for file in self.pathAndFile:
            self.updateProgress(f'Separiert {file}',3)
            frames = self.splitPdf(file, choosenValues)
            self.updateProgress(f'{len(frames)} Seiten werden reduziert', 7)
            self.reducePictures(frames, choosenValues)
            self.updateProgress(f'{len(frames)} Seiten reduziert', 10)
            self.createNewPdf(frames, file)
        for directory in self.garbageDirs:
            os.rmdir(directory)
        self.pathAndFile = {}
        self.garbageDirs = []
        self.showTree(self.pathAndFile)
    
    def updateProgress(self, labelString:str , progress:int):
        self.progressbar["value"] = progress
        self.progressLab['text'] = labelString
        self.controller.root.update_idletasks()

    def splitPdf(self, file:str, qualityDict:dict):
        fileData = self.pathAndFile[file]
        tempStorage = fileData['path']+r'\temp'
        if not os.path.isdir(tempStorage):
            os.mkdir(tempStorage)
        self.garbageDirs.append(tempStorage)
        pdf = fitz.open(fileData['progPath'])
        frames = []
        i = 1
        for frame in pdf.pages():
            pix = frame.get_pixmap(dpi = qualityDict['dpi'])
##            self.updateProgress(f'Seite {i} gefunden',5)
            fileEnding = ['jpg' if qualityDict['mode']=="L" else 'png']
            frameName = f'{tempStorage}//{file}_page_{i}.{fileEnding[0]}'
            pix.save(frameName)
            frames.append(frameName)
            i+=1
        return frames

    def reducePictures(self, frames:list, qualityDict:dict):
        i = 1
        for frame in frames:
            self.updateProgress(f'Seite {i} reduziert',5)
            img = Image.open(frame)
            width,height = img.size
            ratio = width/qualityDict['size']
            img = img.resize((int(width/ratio),int(height/ratio)),
                             Image.ANTIALIAS)
            img = img.convert(qualityDict['mode'])
            img.save(frame, dpi = (qualityDict['dpi'],qualityDict['dpi']),
                     optimize=True, quality=qualityDict['quality'])
            i+=1
        return

    def createNewPdf(self, frames:list, file:str):
        newPdf = fitz.open()
        fileData = self.pathAndFile[file]
        for frame in frames:
            img = fitz.open(frame)
            rect = img[0].rect
            pdfbytes = img.convert_to_pdf()
            img.close()
            imgPDF = fitz.open("pdf", pdfbytes)
            page = newPdf.new_page(width = rect.width,  
                           height = rect.height)
            page.show_pdf_page(rect, imgPDF, 0)
        for frame in frames:
            os.remove(frame)
        newPdf.save(f'{fileData["path"]}/Converted_{file}.pdf', deflate = True)

