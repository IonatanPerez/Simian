import os
try:
	os.chdir(os.path.join(os.getcwd(), 'Selenium'))
	print(os.getcwd())
except:
	pass

# Nota: para que esto funcion hay que tener el archivo https://github.com/mozilla/geckodriver/releases
# en la carpeta del path, que en windows es user/appdata/windows/windowsapp o algo asi.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium

# Pensamos en la estructura de la info

# Queremos recolectar la info disponible de cada autor de LN aprovechando que tienen una pagina donde
# estan todas sus notas indexadas. 

# La estructura de datos para cada autor va a ser la siguiente:

    # Nombre (STR) -- Nombre completo del autor extraido de la pagina
    # URL (STR) -- URL de la pagina que se esta analizando
    # Medio (STR) -- Medio para el cual escribe el autor que se indica en la pagina 
    # Bio (Long STR) -- Bio extraida de la pagina, puede ser un texto largo o puede no haberlo
    # Notas (LST) -- Listado de notas, aca hay que ver todavia que estructura van a tener la info de las notas, por ahora van las URL


# Configuramos el navegador
ffprofile = webdriver.FirefoxProfile()
driver = webdriver.Firefox()

# Generamos la url
# La nacion usa un codigo interno que ignora el nombre del autor, lo que le importa es el ultimo numero
# una pagina de la forma https://www.lanacion.com.ar/autor/test-id va a recuperar todas las notas del autor numero id
# Haciendo una revision rapida, al 26/10/19 tienen hasta el id 13170, al parecer de corrido pero no esta chequeado.

id = 1
moreAutores = True
infoAutores = []

while moreAutores:
    infoAutor = {}
    url = "https://www.lanacion.com.ar/autor/id-"+str(id)
    driver.get(url)

    # Extraemos el nombre del autor
    infoAutor["Nombre"] = driver.title.split("-")[1][1:]
    print (driver.title.split("-")[1])
    assert "Autor" in driver.title
    elem = driver.find_element_by_partial_link_text('VER MÁS NOTAS')
    more = True
    while more:
        try:
            elem.click()
        except Exception as ex:
            more = False
            if type(ex).__name__ == "ElementNotInteractableException":
                print ("Scrolling finalizado bien")
            else:
                raise
    input("Press Enter to continue...")
    infoAutores.append(infoAutor)
    moreAutores = False

driver.close()
print(infoAutores)            



