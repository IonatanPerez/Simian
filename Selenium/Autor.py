from Settings import localfolder, batchLN, numeroDeIntentosDeBusquedaPorAutor
import datetime
import os
import json

def myconverter(o):
    if isinstance(o, (datetime.datetime, datetime.date)):
        return o.isoformat()

class Autor():

    def __init__ (self,id):
        self.id = id
        if os.path.exists(self.path()):
            with open(self.path()) as json_file:
                self.infoAutor = json.load(json_file)
            self.log("Loading data")
            self.log("Last run was the: " + str(self.infoAutor["lastRun"]))
            self.infoAutor["lastRun"] = datetime.datetime.now()
        else:
            self.infoAutor = {}
            self.infoAutor["Id"] = self.id
            self.infoAutor["messagelog"] = []
            self.infoAutor["lastRun"] = datetime.datetime.now()
            self.infoAutor["notas"] = {} # Es un dict y buscamos por id de la nota
            self.infoAutor["notasVacias"] = 0
            self.log("starting new records, time: " + str(datetime.datetime.now()))   
        self.notasUltimaBusqueda = 0
        self.intentosDeBusqueda = 0

    def log(self,string):
        self.infoAutor["messagelog"].append(string)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == None:
            self.log("Final del relevamiento del autor en orden")
            self.infoAutor["FinalizadoCorrectamente"] = True
        else:
            self.log("Final inesperado")
            self.infoAutor["FinalizadoCorrectamente"] = False
            self.log(exc_type)
            self.log(exc_value)
        self.saveToDisk()

    def saveToDisk(self):
        with open(self.path(), 'w') as fp:
            json.dump(self.infoAutor, fp, default=myconverter)     
   
    def path(self):
        return localfolder + "autor_" + str(self.id) + ".json"

    def setValue(self,nombre,valor):
        self.infoAutor[nombre] = valor

    def getValue(self,nombre):
        return self.infoAutor[nombre]

    def validarNumeroDeNotas(self,numeroDeNotas):
        if numeroDeNotas%batchLN == 0: # Da un numero sospechoso 
            if not self.notasUltimaBusqueda == numeroDeNotas: # Y diferente a la busqueda anterior (la primera vez es 0 y busca de nuevo)
                self.notasUltimaBusqueda = numeroDeNotas
                self.log("Parece que no se cargo bien la lista de notas, notas encontradas: " + str(numeroDeNotas))
                self.infoAutor["FinalizadoCorrectamente"] = False
                self.intentosDeBusqueda += 1
                if self.intentosDeBusqueda <= numeroDeIntentosDeBusquedaPorAutor:
                    return False
        else:
            self.intentosDeBusqueda = 0
            self.notasUltimaBusqueda = 0
        return True

    def agregarInfoNota(self,infoNota):
        idNota = infoNota["Id"]
        if not idNota:
            idNota = str(self.infoAutor["notasVacias"]) + "_vacia"
            self.infoAutor["notasVacias"] += 1
        self.infoAutor["notas"][idNota] = infoNota