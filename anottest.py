import fitz
import re
import os
import pyautogui as ag
import pyperclip
import time

folder = r'\\wsrvdms\office\mensching plus StB GmbH\Fristenkontrolle - wöchentlich'

def get_names(file):
    pdf = fitz.open(file)
    names = []
    for page in pdf.pages():
        for annot in page.annots():
            text =annot.info['content']
            foundNames = re.findall('\d \w+, \w+ \d',text)
            for name in foundNames:
                name = re.sub('\s?\d\s?','', name)
                names.append(name)
    return set(names)

def input_names(nameList):
    for name in nameList:
        lastN, firstN = name
        text = f'{firstN} {lastN}'
        pyperclip.copy(text)
        ag.hotkey('ctrl','v')
        ag.hotkey('enter')
        time.sleep(0.3)

            
if __name__ == '__main__':
    walk=  os.walk(folder)
    names = []
    for root, dirs,files in walk:
        for file in files:
            if os.path.splitext(file)[1].lower() == '.pdf':
                names +=  get_names(root+ '\\'+file)
    for i in range(len(names)):
        names[i] = names[i].split(', ')

        
                
    
