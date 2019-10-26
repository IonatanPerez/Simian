#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'Selenium'))
	print(os.getcwd())
except:
	pass

#%%
# Nota: para que esto funcion hay que tener el archivo https://github.com/mozilla/geckodriver/releases
# en la carpeta del path, que en windows es user/appdata/windows/windowsapp o algo asi.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium

# Pensamos en la estructura de la info

# Queremos recolectar la info disponible de cada autor de LN aprovechando que tienen una pagina donde
# estan todas sus notas indexadas. 


# Configuramos el navegador
ffprofile = webdriver.FirefoxProfile()
driver = webdriver.Firefox()

#adblockfile = 'adblock_plus.xpi'
#ffprofile.add_extension(adblockfile)
#driver = webdriver.Firefox(ffprofile)

# Generamos la url
# La nacion usa un codigo interno que ignora el nombre del autor, lo que le importa es el ultimo numero
# una pagina de la forma https://www.lanacion.com.ar/autor/test-id va a recuperar todas las notas del autor numero id
# Haciendo una revision rapida, al 26/10/19 tienen hasta el id 13170, al parecer de corrido pero no esta chequeado.

id = 1
url = "https://www.lanacion.com.ar/autor/id-"+str(id)
driver.get(url)
print (driver.title)
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
driver.close()


