import requests
from bs4 import BeautifulSoup
import time
import datetime
import json
import os

class Clarin:
    
    myname = "Clarin"
    savefolder = "./dataClarin/"
    rawdata = "raw/"
    
    class Home:
    
        url = "https://www.clarin.com/"
       
    
        def __init__ (self):
            self.page = requests.get(self.url)
            if self.page.status_code != 200:
                print (self.page.status_code)
            else:
                print ("Home de " + Clarin.myname + " descargado con exito.")
            self.bpage = BeautifulSoup(self.page.content, 'html.parser')

        def searchthings(self):
            # TODO. Ver que onda https://www.clarin.com/ultimas-noticias/
            # TODO. Ver que onda https://www.clarin.com/noticias-mas-leidas/
            
            pass
    
    def searchHome(self):
        info = {}
        info["timestampofsearch"] = datetime.datetime.now().timestamp()
        info["timeofsearch"] = datetime.datetime.fromtimestamp(info["timestampofsearch"]).isoformat()
        info["filename"] = self.savefolder + self.rawdata + datetime.datetime.fromtimestamp(info["timestampofsearch"]).strftime("%Y-%m-%d-%H-%M") + "-TemperaturaClarin.json"
        
        home = self.Home()
        
        infoTemperatura = home.bpage.find_all(attrs={"class":"temperatura"})
        assert len(infoTemperatura) == 1, "La busqueda de temperatura no encontro lo esperado"
        info["temperatura"]=infoTemperatura[0].contents[0]
        info["sensacion_termica"]=infoTemperatura[0].contents[1].contents[0]
        with open(info["filename"], 'w') as f:
            json.dump(info, f)
        
    # Inicializa las carpetas si no existen
    if not os.path.exists(savefolder):
        os.makedirs(savefolder)
    if not os.path.exists(savefolder+rawdata):
        os.makedirs(savefolder+rawdata)
    
    
def main():
    clarin = Clarin()
    while True:
        clarin.searchHome()
        time.sleep(300)
        
main()