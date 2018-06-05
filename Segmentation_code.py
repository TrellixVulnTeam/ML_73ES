# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 18:50:39 2018

@author: GUPTA50
"""

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import json
import nltk
from nltk.corpus import stopwords
from PyPDF2 import PdfFileReader
from nltk import ngrams
import pickle


fp = open('~//MachineLearning//test.pdf', 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
   raise "Not extractable"

rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

class Point(object):

    def __init__(self,x,y):
        self.x=x
        self.y=y

class Location(object):
  
    def __init__(self,x1,y1,x2,y2):
        self.leftpoint=Point(x1,y1)
        self.rightpoint=Point(x2,y2)
   

class Font(object):

    def __init__(self,myFontName,myFontSize):
        self.FontName=myFontName
        self.FontSize=myFontSize
        
class Character(object):
    def __init__(self,location,font,value):
        self.location=location
        self.font=font
        self.value=value
    def read_character(location,font,value):
        self.location=location
        self.font=font
        self.value=value
        
class Word(object):
   
    def __init__(self,listofCharacters,location,value):
        self.listofCharacters=listofCharacters
        self.location=location
        self.value=value
    def __getListCount__(self):
        val = 0
        val = self.listofCharacters.count
        return val
    
class Line(object):
    def __init__(self,listofWords,location,value):
        self.listofWords=listofWords
        self.location=location
        self.value=value
        
class Page(object):
    listofLines = []
    page_number=0
    def __init__(self,listofLines,page_number):
        self.listofLines=listofLines
        self.page_number=page_number
    
        
class Document(object):
    listofPages = []
    def __init__(self,listofPages):
        self.listofPages=listofPages
        
page_num = 0
docobj = Document([])

if __name__ == "__main__":
    def main_function(objs):
        pageobj = Page([],page_num)
        docobj.listofPages.append(pageobj)
        #print (pageobj.page_number,pageobj.listofLines)
        #docobj.listofPages.append(pageobj)
        for obj in objs:
                if isinstance(obj, pdfminer.layout.LTTextBox):
                    #lineobj = Line([],Location(0,0,0,0))
                    for o in obj:
                        if isinstance(o,pdfminer.layout.LTTextLine):
                            text=o.get_text()
                            lineobj = Line([],Location(o.bbox[0],o.bbox[1],o.bbox[2],o.bbox[3]),text)
                            pageobj.listofLines.append(lineobj)
                            if text.strip():
                                str1 = ''
                                wordobj = Word([],Location(0,0,0,0),"")
                                for c in o._objs:
                                    if isinstance(c, pdfminer.layout.LTChar):
                                        if(c._text != ' '):
                                           str1 = str1 + c._text
                                           charobj = Character(Location(c.bbox[0],c.bbox[1],'',''),Font(c.fontname,c.size),c._text)
                                           wordobj.listofCharacters.append(charobj)
                                        else:
                                            if(len(str1) != 0):
                                                wordobjtemp = wordobj.listofCharacters[0]
                                                wordobj.location.leftpoint = wordobjtemp.location.leftpoint
                                                wordobjtemp = wordobj.listofCharacters[len(wordobj.listofCharacters)-1]
                                                wordobj.value = str1
                                                wordobj.location.rightpoint.x = c.bbox[0]
                                                wordobj.location.rightpoint.y = c.bbox[1]
                                                print(wordobj.value,wordobj.location.leftpoint.x,wordobj.location.leftpoint.y,wordobj.location.rightpoint.x,wordobj.location.rightpoint.y)
                                                lineobj.listofWords.append(wordobj)
                                                #print (lineobj)
                                                wordobj = Word([],Location(0,0,0,0),"")
                                                str1 = ''
                                                continue
                                    else:
                                            if(len(str1) != 0):
                                                wordobjtemp = wordobj.listofCharacters[0]
                                                wordobj.location.leftpoint = wordobjtemp.location.leftpoint
                                                wordobjtemp = wordobj.listofCharacters[len(wordobj.listofCharacters)-1]
                                                wordobj.value = str1
                                                wordobj.location.rightpoint.x = obj.bbox[2]
                                                wordobj.location.rightpoint.y = obj.bbox[1]
                                                print(wordobj.value,wordobj.location.leftpoint.x,wordobj.location.leftpoint.y,wordobj.location.rightpoint.x,wordobj.location.rightpoint.y)
                                                lineobj.listofWords.append(wordobj)
                                                wordobj = Word([],Location(0,0,0,0),"")
                                                str1 = ''
                                                continue
                            #print (lineobj.value,lineobj.listofWords)                
                else:
                    pass
        #print (pageobj.listofLines,pageobj.page_number)        

    for page in PDFPage.create_pages(document):

    # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()
        page_num = page_num + 1
        #print (layout)
        main_function(layout._objs)
    #print (Page.listofLines)
    #print (Page.listofLines,Line.listofWords,Word.listofCharacters)
#print (docobj.listofPages)