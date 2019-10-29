# Nota: para que esto funcion hay que tener el archivo https://github.com/mozilla/geckodriver/releases
# en la carpeta del path, que en windows es user/appdata/windows/windowsapp o algo asi.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
import json
import os


# settings
localfolder = "./Selenium/raw/"
scrappingFile = localfolder + "scrappingLog.json"
nroAutoresLimite = 10 # Asumimos que cuando hay 10 ids consecutivos sin info es que se acabo la lista de autores. 
batchSize = 10 # Cuando se junto la info de 10 autores se vuelca a disco en un archivo aparte.


# Pensamos en la estructura de la info

# Queremos recolectar la info disponible de cada autor de LN aprovechando que tienen una pagina donde
# estan todas sus notas indexadas. 

# La estructura de datos para cada autor va a ser la siguiente:

    # Nombre (STR) -- Nombre completo del autor extraido de la pagina
    # Id (Int) -- Id interno de LN para el autor
    # URL (STR) -- URL de la pagina que se esta analizando
    # Medio (STR) -- Medio para el cual escribe el autor que se indica en la pagina 
    # Bio (Long STR) -- Bio extraida de la pagina, puede ser un texto largo o puede no haberlo
    # FotoUrl (STR) -- Url de la foto
    # FotoId (INT) -- Id de la foto para eventualmente identificar imagenes descargadas. LN usa un servidor de fotos 
    #                 con un formato que es el siguiente https://bucket[1,2,3].glanacion.com/anexos/fotos/[id[-2:]]/[id]h[altoenpixeles].jpg
    # Notas (LST) -- Listado de notas, aca hay que ver todavia que estructura van a tener la info de las notas, por ahora van las URL
    # NotasEncontradas (INT) -- Cantidad de notas encontradas


# La nacion usa un codigo interno que ignora el nombre del autor, lo que le importa es el ultimo numero
# una pagina de la forma https://www.lanacion.com.ar/autor/test-id va a recuperar todas las notas del autor numero id
# Haciendo una revision rapida, al 26/10/19 tienen hasta el id 13170, al parecer de corrido pero no esta chequeado.


# Inicializamos ciertas variables 
nroAutoresAcumulados = 0 # Numero de ids sin info consecutiva

# Iniciamos las variables relacionadas al scrapping porque es comun que se corte y queremos poder retomar.
if os.path.exists(scrappingFile):
    with open(scrappingFile) as json_file:
        infoScrapping = json.load(json_file)
else:
    infoScrapping = {}
    infoScrapping["nextId"] = 1
id = infoScrapping["nextId"]

# Actualizamos el nombre del archivo de autores
authorsFile = localfolder + "authors_" + str((id//10)*10) + ".json"

# Cargamos la info ya guardada de autores
if os.path.exists(authorsFile):
    with open(authorsFile) as json_file:
        infoAutores = json.load(json_file)
else:
    infoAutores = []

print (authorsFile)
# Entramos al loop principal donde interactua con la web. Como suele haber problemas debido
# al caracter dinamico de la pagina, si se corta graba el avance.
try:
    driver = webdriver.Firefox()
    while nroAutoresAcumulados < nroAutoresLimite:
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
                    numeroDeScrolls = 0
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
        for nota in notas:
            InfoNota = {}  
            InfoNota["IdAutor"] = id
            InfoNota["Link"] = nota.find_element_by_tag_name("h2").find_element_by_tag_name("a").get_attribute("href")
            assert InfoNota["Link"].split("-")[-1][:3] == "nid" # Chequeamos que este leyendo el id de la nota
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

        print (infoAutor)
        infoAutores.append(infoAutor)


        # Si acumulamos 10 autores hacemos el volcado a disco y limpiamos la lista
        if id//batchSize == 0:
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