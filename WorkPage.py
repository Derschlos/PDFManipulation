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
        self.dimensions = '672x455'
        self.config(bg = self.bg,)
        self.controller = controller
        self.controller.pathAndFile = {}
        self.garbageDirs = []
        


    
    
    # Widgets
        self.progressbar = ttk.Progressbar(self,
                                 orient='horizontal',
                                 mode='determinate',
                                 maximum = 10)
        self.textFrame = tk.Frame(self, bg=self.bg)
        self.statusText = tk.Text(self.textFrame,state='disabled', )
        self.statusTextYScroll = tk.ttk.Scrollbar(self.textFrame, orient = 'vertical', command = self.statusText.yview)
        self.statusText['yscrollcommand'] = self.statusTextYScroll.set
        self.returnBut = tk.Button(self, text = 'Zurück zur Auswahl', 
                                   command= self.returnToSelection, 
                                   state= 'disabled')


    # Grid
        self.textFrame.grid(column  = 1, row = 1, padx=5, pady=5)
        self.statusText.grid(column  = 1, row = 1)
        self.statusTextYScroll.grid(column  = 2, row = 1,
                                    sticky = ('n','s','w'))
        self.progressbar.grid(column  = 1, row = 2,
                           sticky= ('e','w'), columnspan=2,
                           padx = 3)
        self.returnBut.grid(column  = 1, row = 3,
                           sticky= ('e','w'), columnspan = 2,
                           padx = 3, pady = 5)


    def onRaise(self):
        self.controller.root.title('Work Page')
        self.controller.root.geometry(self.dimensions)
        self.controller.root.update_idletasks()
        self.controller.root.after_idle(self.minify)

    def insertText(self,text:str):
        self.statusText['state'] = 'normal'
        self.statusText.insert('end', text)
        self.statusText.insert('end', '\n')
        self.statusText.see('end')
        self.statusText['state'] = 'disabled'
        
    def returnToSelection(self):
        self.statusText['state'] = 'normal'
        self.statusText.delete('1.0', 'end')
        self.statusText['state'] = 'disabled'
        self.controller.showSelectionFrame()
        self.returnBut['state'] = 'disabled'

    # Main creation Logic
    def minify(self):       
        for file in self.controller.pathAndFile:
            self.updateProgress(f'Neue Datei {file}', 0)
            self.updateProgress(f'Trennt "{file}" in einzelnde Seiten',3)
            frames = self.splitPdf(file, self.controller.qualityValues)
            self.updateProgress(f'{len(frames)} Seiten werden reduziert', 7)
            self.reducePictures(frames, self.controller.qualityValues)
            self.updateProgress(f'{len(frames)} Seiten von {file} reduziert', 10)
            self.createNewPdf(frames, file)
        for directory in self.garbageDirs:
            self.updateProgress(f'Löscht folgende Temp Ordner: {self.garbageDirs}', 10)
            os.rmdir(directory)
        self.controller.pathAndFile = {}
        self.garbageDirs = []
        self.controller.updateSelectionPage()
        self.returnBut['state'] = 'normal'
        
    
    def updateProgress(self, text:str , progress:int):
        self.progressbar["value"] = progress
        self.insertText(text)
        self.controller.root.update()

    def splitPdf(self, file:str, qualityDict:dict):
        fileData = self.controller.pathAndFile[file]
        tempStorage = fileData['path']+r'/temp'
        if not os.path.isdir(tempStorage):
            os.mkdir(tempStorage)
        self.garbageDirs.append(tempStorage)
        pdf = fitz.open(fileData['progPath'])
        frames = []
        i = 1
        for frame in pdf.pages():
            pix = frame.get_pixmap(dpi = qualityDict['dpi'])
            self.updateProgress(f'Seite {i} gefunden',5)
            fileEnding = ['jpg' if qualityDict['mode']=="L" else 'png']
            frameName = f'{tempStorage}//{file}_page_{i}.{fileEnding[0]}'
            pix.save(frameName)
            frames.append(frameName)
            i+=1
        return frames

    def reducePictures(self, frames:list, qualityDict:dict):
        i = 1
        for frame in frames:
            self.updateProgress(f'Seite {i} reduziert',9)
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
        fileData = self.controller.pathAndFile[file]
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

