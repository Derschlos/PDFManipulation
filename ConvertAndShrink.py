# -*- coding: utf-8 -*-

# venv = r""

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk
import re
##import os
##import math
##from PIL import Image, ImageEnhance
from tkinter.messagebox import showwarning
import fitz
import time
from multiprocessing import Pool, freeze_support
from SelectionPage import SelectionPage
from WorkPage import WorkPage
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
            self.frames[frame.pageName] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.showFrame('SelectionPage')
        
    def showFrame(self,frameName):
        frame= self.frames[frameName]
        frame.tkraise()
        frame.onRaise()

        







if __name__ == '__main__':
    root= TkinterDnD.Tk()
    basedesk(root)
    root.mainloop()
