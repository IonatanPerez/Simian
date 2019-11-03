from Settings import scrappingFile, nroAutoresLimiteNulos
import os
import json
import datetime

def myconverter(o):
    if isinstance(o, (datetime.datetime, datetime.date)):
        return o.isoformat()

class Scrapping():
    def __init__ (self):
        if os.path.exists(scrappingFile):
            with open(scrappingFile) as json_file:
                self.infoScrapping = json.load(json_file)
            self.log("Loading data")
            self.log("Last run was the: " + str(self.infoScrapping["lastRun"]))
            self.infoScrapping["lastRun"] = datetime.datetime.now()
            self.log("Last run runs until id: " + str(self.infoScrapping["IdAutor"]))
        else:
            self.infoScrapping = {}
            self.infoScrapping["messagelog"] = []
            self.infoScrapping["lastRun"] = datetime.datetime.now()
            self.log("starting new records, time: " + str(datetime.datetime.now()))   
        self.infoScrapping["IdAutor"] = 1
        self.nroAutoresNulos = 0
        self.idActual = self.infoScrapping["IdAutor"]
        
    def seguirBusqueda (self):
        if self.nroAutoresNulos < nroAutoresLimiteNulos:
            return True
        else:
            return False

    def log(self,string):
        self.infoScrapping["messagelog"].append(string)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == None:
            self.log("Final del scrapping en orden")
        else:
            self.log("Final inesperado")
            self.log(exc_type)
            self.log(exc_value)
        self.saveToDisk()

    def saveToDisk(self):
        with open(scrappingFile, 'w') as fp:
            json.dump(self.infoScrapping, fp, default=myconverter)   

    def nextAutor(self):
        self.saveToDisk()
        self.infoScrapping["IdAutor"] += 1
        self.idActual = self.infoScrapping["IdAutor"]

    def autorNoEncontrado(self):
        self.log("No se ha encontrado al autor: " + self.idActual)
        self.nroAutoresNulos += 1
        self.nextAutor()
    
    def autorEncontrado(self):
        self.nroAutoresNulos = 0
   
   
    