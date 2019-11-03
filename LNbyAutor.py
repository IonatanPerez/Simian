# Nota: para que esto funcion hay que tener el archivo https://github.com/mozilla/geckodriver/releases
# en la carpeta del path, que en windows es user/appdata/windows/windowsapp o algo asi.
from selenium import webdriver
import selenium
import Scrapping
import Autor
import time
import Settings
from tqdm import tqdm


with Scrapping.Scrapping() as scrp:
    driver = webdriver.Firefox()
    while scrp.seguirBusqueda():
        with Autor.Autor(scrp.idActual) as autor:
            url = "https://www.lanacion.com.ar/autor/id-"+str(scrp.idActual)
            driver.get(url)
            assert "Autor" in driver.title
            if driver.title == "Autor - - LA NACION":
                scrp.autorNoEncontrado()
                continue
            else:
                scrp.autorEncontrado()
            
            # Extraemos el nombre del autor
            autor.setValue("Nombre",driver.title.split("-")[1][1:][:-1])
            autor.setValue("Id",scrp.idActual)
            autor.setValue("Url",url)

            # Buscamos la info de la bio
            if driver.find_elements_by_class_name("wiki"):
                bio = driver.find_element_by_class_name("wiki")
                autor.setValue("Medio",bio.find_element_by_tag_name ("h2").get_attribute('innerHTML'))
                if driver.find_element_by_class_name("foto").find_elements_by_tag_name('img'):
                    autor.setValue("FotoUrl",driver.find_element_by_class_name("foto").find_element_by_tag_name('img').get_attribute('src'))
                    autor.setValue("FotoId",autor.getValue("FotoUrl").split("/")[-1].split("h")[0])
                else:
                    autor.setValue("FotoUrl",None)
                    autor.setValue("FotoId",None)
                if bio.find_elements_by_class_name ("expandible"):
                    autor.setValue("Bio",bio.find_element_by_class_name ("expandible").get_attribute('innerHTML'))
                else:
                    autor.setValue("Bio",None)
            else:
                autor.setValue("Medio",None)
                autor.setValue("FotoUrl",None)
                autor.setValue("FotoId",None)
                autor.setValue("Bio",None)

            # Antes de escrollear mas notas nos fijamos si vale la pena (si la id de la nota ya esta). 
            # Buscamos el cuerpo de notas
            MoreScrolling = True
            NewNotas = False
            listado = driver.find_element_by_class_name("listado")
            notas = listado.find_elements_by_class_name("nota")
            url1 = notas[0].find_element_by_tag_name("h2").find_element_by_tag_name("a").get_attribute("href")
            if url1 != "https://www.lanacion.com.ar/null":
                notaid1 = url1.split("-")[-1][3:]
                if notaid1 in autor.infoAutor["notas"].keys():
                    NewNotas = False
                    print ("Notas de " + autor.infoAutor["Nombre"] + " (" + str(scrp.idActual) + ") ya cargadas.")
                    autor.log("Salteando cargado de nuevas notas porque no parece haber actualizaciones.")

            for nota in notas:
                url = nota.find_element_by_tag_name("h2").find_element_by_tag_name("a").get_attribute("href")
                if url != "https://www.lanacion.com.ar/null":
                    notaid = url.split("-")[-1][3:]
                    if notaid in autor.infoAutor["notas"].keys():
                        MoreScrolling = False
                        break 

            # Nos fijamos si se pueden escrollear mas notas.
            if MoreScrolling:
                if driver.find_elements_by_partial_link_text('VER MÁS NOTAS'):
                    elem = driver.find_element_by_partial_link_text('VER MÁS NOTAS')
                    more = True
                    while more:
                        try:
                            elem.click()
                            time.sleep(Settings.timewait)
                        except Exception as ex:
                            if type(ex).__name__ == "ElementNotInteractableException":
                                more = False
                            else:
                                if type(ex).__name__ == "ElementClickInterceptedException":
                                    elem.location_once_scrolled_into_view
                                else:
                                    print (type(ex).__name__)
                                    raise

            # Buscamos el cuerpo de notas
            listado = driver.find_element_by_class_name("listado")
            notas = listado.find_elements_by_class_name("nota")
            # Lo que hacemos aca es chequear si el numero de notas encontradas es un multiplo
            # de la cantidad de notas que se cargan por batch. En ese caso sospechamos que 
            # se corto la comuniacion o algo asi (para evitar eso mas arriba se espera a que cargue pero 
            # igual a veces puede fallar). Como puede pasar que justo haya un numero de notas multiplo
            # del batch lo que hacemos es repetir la busqueda a ver si coincide, en ese caso lo damos por
            # valido. 

            if MoreScrolling: # Para no sobreescribir en caso de que ya haya notas previas.
                if not scrp.validarNumeroDeNotas(autor,len(notas)):
                    continue
                autor.setValue("NotasEncontradas",len(notas))
                
            

            if NewNotas:
                for nota in tqdm(notas):
                    InfoNota = {}  
                    InfoNota["IdAutor"] = scrp.idActual
                    InfoNota["Link"] = nota.find_element_by_tag_name("h2").find_element_by_tag_name("a").get_attribute("href")
                    if InfoNota["Link"] == "https://www.lanacion.com.ar/null":
                        autor.log("link inexistente: " + "Autor: " + str(id) + "nota: " + nota.get_attribute("innerHTML"))
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
                    autor.agregarInfoNota(InfoNota)

            
        scrp.nextAutor()