from abstract import Abstract, isabstract
import requests
from bs4 import BeautifulSoup
import os

class Portal(Abstract):
    
    name = isabstract
    url = isabstract

        
    def runoninit(self):
        self.initfolders()
        self.createfolders()
        print ("Por crear home")
        self.gethome()
        print ("Home Creado")

    def initfolders(self):
        self.savefolder = "./data" + self.name + "/"
        self.saverawdatafolder = self.savefolder + "raw/"
        
    def gethome(self):
        self.home = Home(self.url)
        
    def createfolders(self):
        if not os.path.exists(self.savefolder):
            os.makedirs(self.savefolder)
        if not os.path.exists(self.saverawdatafolder):
            os.makedirs(self.saverawdatafolder)

class Home(Abstract):
    
    def __init__(self,url):
        #print ("runinit Home")
        self.page = requests.get(url)
        if self.page.status_code != 200:
            print (self.page.status_code)
        else:
            print (url + " descargada con exito.")
        self.bpage = BeautifulSoup(self.page.content, 'html.parser')
    
    def runoninit(self,url):
        print ("runinit Home")
        self.page = requests.get(url)
        if self.page.status_code != 200:
            print (self.page.status_code)
        else:
            print (url + " descargada con exito.")
        self.bpage = BeautifulSoup(self.page.content, 'html.parser')
    
    def pretty(self):
        print(self.bpage.prettify())
        
