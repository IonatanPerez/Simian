# Nota: para que esto funcion hay que tener el archivo https://github.com/mozilla/geckodriver/releases
# en la carpeta del path, que en windows es user/appdata/windows/windowsapp o algo asi.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import selenium
import json
import time
from tqdm import tqdm
import Scrapping
import Settings


# Inicializamos ciertas variables 
nroAutoresAcumulados = 0 # Numero de ids sin info consecutiva
NotasEncontradasPreviamente = 0 # Esto sirve para verificar si se encontro un numero de notas razonable o si se corto el scrolling
intentosDeBusqueda = 0 # Esta relacionado a los intentos de busqueda en caso de que parezca que no cargo bien la pagina 

# Iniciamos las variables relacionadas al scrapping porque es comun que se corte y queremos poder retomar.
scrap = Scrapping.Scrapping()

# Entramos al loop principal donde interactua con la web. Como suele haber problemas debido
# al caracter dinamico de la pagina, si se corta graba el avance.
try:
    driver = webdriver.Firefox()
    while scrap.seguirBusqueda():
        scrap
        infoAutor = {}
        url = "https://www.lanacion.com.ar/autor/id-"+str(id)
        driver.get(url)
        assert "Autor" in driver.title
        if driver.title != "Autor - - LA NACION":
            nroAutoresAcumulados = 0
        else:
            nroAutoresAcumulados =+ 1
            id = id +1 
            continue
        # Extraemos el nombre del autor
        infoAutor["Nombre"] = driver.title.split("-")[1][1:][:-1]
        infoAutor["Id"] = id
        infoAutor["Url"] = url

        
        # Buscamos la info de la bio
        bio = driver.find_element_by_class_name("wiki")
        infoAutor["Medio"] = bio.find_element_by_tag_name ("h2").get_attribute('innerHTML')
        if driver.find_element_by_class_name("foto").find_elements_by_tag_name('img'):
            infoAutor["FotoUrl"] = driver.find_element_by_class_name("foto").find_element_by_tag_name('img').get_attribute('src')
            infoAutor["FotoId"] = infoAutor["FotoUrl"].split("/")[-1].split("h")[0]
        else:
            infoAutor["FotoUrl"] = None
            infoAutor["FotoId"] = None
        if bio.find_elements_by_class_name ("expandible"):
            infoAutor["Bio"] = bio.find_element_by_class_name ("expandible").get_attribute('innerHTML')
        else:
            infoAutor["Bio"] = None

        # Nos fijamos si se pueden escrollear mas notas.
        if driver.find_elements_by_partial_link_text('VER MÁS NOTAS'):
            elem = driver.find_element_by_partial_link_text('VER MÁS NOTAS')
            more = True
            while more:
                try:
                    elem.click()
                    time.sleep(1)
                except Exception as ex:
                    if type(ex).__name__ == "ElementNotInteractableException":
                        more = False
                    else:
                        if type(ex).__name__ == "ElementClickInterceptedException":
                            elem.location_once_scrolled_into_view
                        else:
                            print (type(ex).__name__)
                            raise


        # Una vez cargada la pagina completa tratamos de extraer el listado de notas.
        # Al parecer la estructura de nombre es similar a la de autores en el sentido de 
        # que lo que importa es el id y el resto del link es irrelevante, excepto por la 
        # seccion, eso hace que en principio no se pueda buscar en forma secuencial. Sin 
        # embargo si recolectamos la lista de todas las secciones posibles, eventualmente
        # se podria probar con el id en todas las secciones.

        # Buscamos el cuerpo de notas
        listado = driver.find_element_by_class_name("listado")
        notas = listado.find_elements_by_class_name("nota")
        
        # Lo que hacemos aca es chequear si el numero de notas encontradas es un multiplo
        # de la cantidad de notas que se cargan por batch. En ese caso sospechamos que 
        # se corto la comuniacion o algo asi (para evitar eso mas arriba se espera a que cargue pero 
        # igual a veces puede fallar). Como puede pasar que justo haya un numero de notas multiplo
        # del batch lo que hacemos es repetir la busqueda a ver si coincide, en ese caso lo damos por
        # valido. 

        if len(notas)%batchLN == 0:
            if len(notas) == NotasEncontradasPreviamente:
                infoAutor["ScrollingCorrecto"] = True
                intentosDeBusqueda = 0
                NotasEncontradasPreviamente = 0
            else:
                NotasEncontradasPreviamente = len(notas)
                infoAutor["ScrollingCorrecto"] = False
                intentosDeBusqueda = intentosDeBusqueda + 1
                if intentosDeBusqueda < 10:
                    infoScrapping["messagelog"].append("Warning! No se logro cargar bien los datos del autor: " + infoAutor["Nombre"] + " id: "+str(infoAutor["Id"]) + " intento nro: " + str(intentosDeBusqueda))
                    print ("Warning! No se logro cargar bien los datos del autor: " + infoAutor["Nombre"] + " id: "+str(infoAutor["Id"]) + " intento nro: " + str(intentosDeBusqueda))
                    continue
                else:
                    intentosDeBusqueda = 0
                    NotasEncontradasPreviamente = 0
        else:
            intentosDeBusqueda = 1      
            NotasEncontradasPreviamente = 0

        
        # Estrucrtura de la info que queremos recolectar:

        # Id (INT) -- Id de la nota
        # IdAutor (INT) -- Id del autor de la nota
        # Link (STR) -- Link a la nota
        # Seccion (STR) -- Seccion, esto es importante para poder saber que secciones hay y testear urls de notas
        # Tema (STR) -- String del tema
        # TemaId (INT) -- Id del tema, los temas al igual que los demas se pueden buscar por fuerza bruta 
        #                   buscando https://www.lanacion.com.ar/tema/test-tid[ID]
        # Imagen (STR) -- Link a la imagen si la hay
        # ImagenId (INT) -- Si lo hay
        # Fecha (STR) -- Viene como STR pero supongo que despues se puede pasar a algo mas procesable

        infoAutor["InfoNotas"] = []
        infoAutor["NotasEncontradas"] = len(notas)
        print ("Procesando: " + infoAutor["Nombre"] + "(" + str(infoAutor["Id"]) + ")" + ", notas a procesar: " + str(len(notas)))
        for nota in tqdm(notas):
            InfoNota = {}  
            InfoNota["IdAutor"] = id
            InfoNota["Link"] = nota.find_element_by_tag_name("h2").find_element_by_tag_name("a").get_attribute("href")
            if InfoNota["Link"] == "https://www.lanacion.com.ar/null":
                infoScrapping["messagelog"].append("link inexistente: " + "Autor: " + str(id) + "nota: " + nota.get_attribute("innerHTML"))
                InfoNota["Id"] = None
            else:
                assert InfoNota["Link"].split("-")[-1][:3] == "nid", nota.get_attribute("innerHTML") # Chequeamos que este leyendo el id de la nota
                InfoNota["Id"] = InfoNota["Link"].split("-")[-1][3:]
            InfoNota["Seccion"] = "/".join(InfoNota["Link"].split("/")[3:][:-1])
            if nota.find_elements_by_tag_name("h3"):
                InfoNota["Tema"] = nota.find_element_by_tag_name("h3").text
                InfoNota["TemaId"] = nota.find_element_by_tag_name("h3").find_element_by_tag_name("a").get_attribute("href").split("-")[-1]
            else:
                InfoNota["Tema"] = None
                InfoNota["TemaId"] = None
            if nota.find_elements_by_tag_name("img"):
                InfoNota["Imagen"] = nota.find_element_by_class_name("figure").find_element_by_tag_name("img").get_attribute("src")
                InfoNota["ImagenId"] = InfoNota["Imagen"].split("/")[-1].split("h")[0]
            else:
                InfoNota["Imagen"] = None
                InfoNota["ImagenId"] = None
            if nota.find_elements_by_class_name("fecha"):
                InfoNota["Fecha"] = nota.find_element_by_class_name("fecha").text
            else:
                InfoNota["Fecha"] = None
            infoAutor["InfoNotas"].append(InfoNota)

        infoAutores.append(infoAutor)


        # Si acumulamos 10 autores hacemos el volcado a disco y limpiamos la lista
        if id%batchSize == 0:
            print ("Volcando a disco el archivo" + authorsFile)
            with open(authorsFile, 'w') as fp:
                json.dump(infoAutores, fp)
            infoAutores = []
            authorsFile = localfolder + "authors" + str((id//10)*10) + ".json"

        infoScrapping["nextId"] = id + 1
        id = id + 1                  
        with open(scrappingFile, 'w') as fp:
            json.dump(infoScrapping, fp)
        
    print ("ejecucion terminada con exito")
    with open(authorsFile, 'w') as fp:
        json.dump(infoAutores, fp) 
    with open(scrappingFile, 'w') as fp:
        json.dump(infoScrapping, fp)     
        
except:
    print ("Final inesperado")
    with open(authorsFile, 'w') as fp:
        json.dump(infoAutores, fp)     
    with open(scrappingFile, 'w') as fp:
        json.dump(infoScrapping, fp)     
    raise