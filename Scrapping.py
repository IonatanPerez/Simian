from Settings import scrappingFile, nroAutoresLimiteNulos, batchLN, numeroDeIntentosDeBusquedaPorAutor, startOnId
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
        if startOnId:
            self.infoScrapping["IdAutor"] = startOnId
        
        self.recuperando = True
        self.nroAutoresNulos = 0
        self.idActual = self.infoScrapping["IdAutor"]
        self.intentosDeBusqueda = 0
        self.notasUltimaBusqueda = 0
        
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
        self.log("No se ha encontrado al autor: " + str(self.idActual))
        self.nroAutoresNulos += 1
        self.nextAutor()
    
    def autorEncontrado(self):
        self.nroAutoresNulos = 0
   
    def validarNumeroDeNotas(self,autor,numeroDeNotas):
        if numeroDeNotas%batchLN == 0: # Da un numero sospechoso 
            if not self.notasUltimaBusqueda == numeroDeNotas: # Y diferente a la busqueda anterior (la primera vez es 0 y busca de nuevo)
                self.notasUltimaBusqueda = numeroDeNotas
                autor.log("Parece que no se cargo bien la lista de notas, notas encontradas: " + str(numeroDeNotas))
                autor.infoAutor["FinalizadoCorrectamente"] = False
                self.intentosDeBusqueda += 1
                if self.intentosDeBusqueda <= numeroDeIntentosDeBusquedaPorAutor:
                    return False
        else:
            self.intentosDeBusqueda = 0
            self.notasUltimaBusqueda = 0
        return True
