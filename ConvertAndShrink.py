# -*- coding: utf-8 -*-

# venv = r""

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk
import re
import os
import math
from PIL import Image, ImageEnhance
from tkinter.messagebox import showwarning
import fitz
import time
from PyInstaller.utils.hooks import collect_data_files, eval_statement
datas = collect_data_files('tkinterdnd2')



def getLBString(listbox):
    try:
        return listbox.get(listbox.curselection()[0])
    except:
        return ''

class basedesk:
    def __init__(self,root):
        self.root = root
        self.root.config()
        self.root.title('Base page')
        self.root.geometry('660x200')
        self.baseContainer = tk.Frame(self.root)
        self.baseContainer.pack(side = "top", fill = "both", expand = True)
        self.baseContainer.grid_rowconfigure(0, weight = 1)
        self.baseContainer.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for f in (SelectionPage,WorkPage):
            frame = f(self.baseContainer, self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.showFrame(SelectionPage)
        
    def showFrame(self,frameName):
        frame= self.frames[frameName]
        frame.tkraise()
        frame.onRaise()

class SelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
##        self.config()
        self.style = ttk.Style()
        self.bg = 'lightsalmon'
        self.config(bg = self.bg,)
        self.controller = controller
        self.pathAndFile = {}
        self.garbageDirs = []
        self.garbageFiles = []

        
        self.modeVar = tk.StringVar()
        self.dpiVar = tk.IntVar(value=300)
        self.qualiVar = tk.StringVar(value = 65)
        self.sizeVar = tk.StringVar(value = 800)

    #widgets
        self.tree = ttk.Treeview(self,
                                 show='headings',
                                 columns = ('name','size'),
                                 height = 7,)
        self.tree.heading('name', text = "Name",)
        self.tree.heading('size', text = "Größe in KB")
        self.tree.column('#2', width = 80, anchor = 'center')
        self.tree.column('#1', stretch = True)

        # Mode Radiobuttons
        self.radioFrame = tk.Frame(self, bg = self.bg)
        self.blackWhite = tk.Radiobutton(self.radioFrame, text = "Schwarz/Weiß", variable = self.modeVar, value = "1", bg = self.bg)
        self.greyScale = tk.Radiobutton(self.radioFrame, text = "Grau", variable = self.modeVar, value = "L", bg = self.bg)
        self.greyScale.invoke()

        # Quality, DPI and PageSize Entrys
        self.qualiFrame = tk.Frame(self,bg = self.bg)
        self.dpiLabel = tk.Label(self.qualiFrame, text = 'DPI:',bg= self.bg)
        checkNumWrapper = (self.controller.root.register(self.checkDpiSizeNum),
                           '%P')
        checkQauliNumWrapper = (self.controller.root.register(self.checkQualiNum),
                           '%P')
        self.dpiEntry = tk.Entry(self.qualiFrame,
                                 textvariable=self.dpiVar,
                                 validate='key',
                                 validatecommand = checkNumWrapper)
        self.qualiLabel = tk.Label(self.qualiFrame,
                                   text = "Qualität (%): ",
                                   bg = self.bg)
        self.qualiEntry = tk.Entry(self.qualiFrame,
                                   textvariable = self.qualiVar,
                                   validate='key',
                                   validatecommand = checkQauliNumWrapper)
        self.sizeLable = tk.Label(self.qualiFrame,
                                  text = "Seitengröße:",
                                  bg = self.bg)
        self.sizeEntry = tk.Entry(self.qualiFrame,
                                  textvariable = self.sizeVar,
                                  validate='key',
                                  validatecommand = checkNumWrapper)
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
        # Button Frame
        self.buttonFrame = tk.Frame(self,bg = self.bg)
        self.startBut = tk.Button(self.buttonFrame,
                                  text = "Dokumente reduzieren",
                                  command = self.minify)
        self.deletePDF = tk.Button(self.buttonFrame,
                                  text = "Dokument löschen",
                                  command = self.delete)
        
        
    #bindings
        self.controller.root.drop_target_register(DND_FILES)
        self.controller.root.dnd_bind('<<Drop>>',lambda e: self.addPdf(e.data))


    #postition
        self.tree.grid(column  = 3, row = 1,
                       rowspan = 3,
                       pady = 5, padx = 5,)
        self.radioFrame.grid(column  = 1, row = 0,
                             rowspan = 2,
                             padx = 5,
                             sticky = 'w')
        self.blackWhite.grid(column  = 1, row = 1,
                             padx = 5,
                             sticky = 'w')
        self.greyScale.grid(column  = 1, row = 2,
                            padx = 5,
                            sticky = 'w')
        # Button grid
        self.buttonFrame.grid(column  = 1, row = 2,
                              columnspan = 2,
                              padx = 5, sticky = 'w')
        self.startBut.grid(column  = 1, row = 1,)
        self.deletePDF.grid(column  = 2, row = 1, padx = 15)
        # Quali grid
        self.qualiFrame.grid(column  = 2, row = 1,
                             padx = 5, pady = 10,
                             sticky = 'n')
        self.dpiLabel.grid(column  = 1, row = 1,
                           padx = 5,
                           sticky = 'w')
        self.dpiEntry.grid(column  = 2, row = 1,
                           padx = 5,
                           sticky = 'we')
        self.sizeLable.grid(column  =1, row = 2,
                            padx = 5,
                            sticky = 'w')
        self.sizeEntry.grid(column  = 2, row = 2,
                            padx = 5,
                            sticky = 'we')
        self.qualiLabel.grid(column  = 1, row = 3,
                             padx = 5,
                             sticky = 'w')
        self.qualiEntry.grid(column  = 2, row = 3,
                             padx = 5,
                             sticky = 'we')
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
        self.controller.root.title('Selection Page')
    def checkDpiSizeNum(self, newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval) <= 3
    def checkQualiNum(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval) <= 2
        
    def delete(self):
        file = self.tree.focus()
        if file == "":
            return
        del self.pathAndFile[file]
        self.showTree(self.pathAndFile)

    
    def addPdf(self,data):
        """Triggers on Drop.
           data = filters out """
        multifile = []
        if '{' in data:
            filesWithSpaces = re.findall('[{][^{}]+[}]',data)
            noSpaceFiles = data
            for file in filesWithSpaces:
                noSpaceFiles = re.sub('[{][^{}]+[}]', '', noSpaceFiles)
                filesWithSpaces[filesWithSpaces.index(file)] = re.sub('[{}]', '',file)
            try: 
                while noSpaceFiles[0] ==' ':
                    noSpaceFiles=noSpaceFiles[1:]
            except:
                noSpaceFiles = ""  #if you only add one File with spaces it would crash here without the try block
        else:
            noSpaceFiles = data
            filesWithSpaces = []
        noSpaceFiles = [file for file in noSpaceFiles.split(' ') if file != '']
        multifile = filesWithSpaces+noSpaceFiles
        for dat in multifile:
            folder,file = os.path.split(dat)
            sizeInKB = math.ceil(os.stat(dat).st_size/1024)
            if ".pdf" in file[-4:len(file)].lower():
                self.pathAndFile[file] ={
                    'path':folder,
                    "progPath":dat,
                    "size":sizeInKB}
            self.showTree(self.pathAndFile)

    def showTree(self, dataDict):
        for child in self.tree.get_children(''):
            self.tree.delete(child)
        for data in dataDict:
            self.tree.insert('',
                             'end',
                             data,
                             values = [data, dataDict[data]['size']])
            self.progressLab['text'] = 'Datei eingefügt'

    # Main creation Logic
    def minify(self):
        self.updateProgress('Neue Datei', 0)
        choosenValues = {'mode':self.modeVar.get(),
                         'dpi':int(self.dpiEntry.get()),
                         'size': int(self.sizeEntry.get()),
                         'quality':int(self.qualiEntry.get())}
        if '' in choosenValues.values():
            showwarning(title = 'Fehlender Wert',
                        message = f'Es fehlen Werte: {[keyName for keyName,value in choosenValues.items() if value == ""]}')
            self.updateProgress('Fehlender Wert', 0)
            return
        for file in self.pathAndFile:
            self.updateProgress(f'Separiert {file}', 2)
            frames = self.splitPdf(file, choosenValues)
            self.updateProgress(f'{len(frames)} Seiten werden reduziert', 3)
            self.reducePictures(frames, choosenValues)
            self.updateProgress(f'{len(frames)} Seiten reduziert', 6)
            self.createNewPdf(frames, file)

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
            frameName = f'{tempStorage}//{file}_page_{i}.jpg'
            pix.save(frameName)
            frames.append(frameName)
            i+=1
        return frames

    def reducePictures(self, frames:list, qualityDict:dict):
        for frame in frames:
            img = Image.open(frame)
            width,height = img.size
            ratio = width/qualityDict['size']
            img = img.resize((int(width/ratio),int(height/ratio)),
                             Image.ANTIALIAS)
            img = img.convert(qualityDict['mode'])
            img.save(frame, dpi = (qualityDict['dpi'],qualityDict['dpi']),
                     optimize=True, quality=qualityDict['quality'])
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



        
class WorkPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config()
##        self.config(bg = 'lightsalmon')
        self.controller = controller

    def onRaise(self):
        self.controller.root.title('Work Page')






if __name__ == '__main__':
    root= TkinterDnD.Tk()
    basedesk(root)
    root.mainloop()
