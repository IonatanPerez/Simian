import os
import shutil
from Settings import processingFolder, localfolder
import json
import pandas as pd
from tqdm import tqdm


def copyfilefromsource():
    src_files = os.listdir(localfolder)
    for file_name in src_files:
        full_file_name = os.path.join(localfolder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, processingFolder)

""" def changeDateFormat():
    archivos = listOfFiles()
    for archivo in archivos[0:1]:
        with open(processingFolder+archivo) as json_file:
            data = json.load(json_file) """

class iterAutores:
    def __init__(self):
        self.archivos = os.listdir(processingFolder)
        self.index = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            archivo = self.archivos[self.index]
            if archivo == "scrappingLog.json":
                raise StopIteration()
            with open(processingFolder+archivo) as json_file:
                data = json.load(json_file)
        except IndexError:
            raise StopIteration()
        self.index += 1
        return data

def listadoUnicoDeNotas():
    listado = []
    for autor in tqdm(iterAutores()):
        if not "notas" in autor:
            print (autor)
        notas = autor["notas"]
        for idnota, nota in notas.items():
            nota[idnota] = idnota
            listado.append(nota)
    return listado

lista = listadoUnicoDeNotas()
df = pd.DataFrame(lista)
pass