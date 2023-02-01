# -*- coding: utf-8 -*-

# venv = r""

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk
from tkinter.messagebox import showwarning
import re

class SelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
##        self.config()
        self.pageName = 'SelectionPage'
        self.style = ttk.Style()
        self.bg = 'lightsalmon'
        self.config(bg = self.bg,)
        self.controller = controller
        self.pathAndFile = {}
        self.garbageDirs = []

        
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
        self.blackWhite = tk.Radiobutton(self.radioFrame,
                                         text = "Schwarz/Weiß",
                                         variable = self.modeVar,
                                         value = "1", bg = self.bg)
        self.greyScale = tk.Radiobutton(self.radioFrame,
                                        text = "Grau",
                                        variable = self.modeVar,
                                        value = "L", bg = self.bg)
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
        choosenValues = {'mode':self.modeVar.get(),
                         'dpi':int(self.dpiEntry.get()),
                         'size': int(self.sizeEntry.get()),
                         'quality':int(self.qualiEntry.get())}
        if '' in choosenValues.values():
            showwarning(title = 'Fehlender Wert',
                        message = f'Es fehlen Werte: {[keyName for keyName,value in choosenValues.items() if value == ""]}')
            self.updateProgress('Fehlender Wert', 0)
            return
        else:
            self.controller.showFrame('WorkPage')
