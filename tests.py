# Testeamos cosas de scraping utilizando este tutorial 
# https://www.dataquest.io/blog/web-scraping-tutorial-python/


# Documentacion que puede ser util
# https://2.python-requests.org//en/master/user/quickstart/#response-content
#%%
import requests
from bs4 import BeautifulSoup

#%%
# Creamos el soup
page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
soup = BeautifulSoup(page.content, 'html.parser')
#%%
# imprimimos la lista de elementos
print (list(soup.children))
#%%
# Nos quedamos con el tercero
out = list(soup.children)[2]
print ("Segundo nivel")
print (out)