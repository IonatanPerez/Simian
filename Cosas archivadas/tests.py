# Testeamos cosas de scraping utilizando este tutorial 
# https://www.dataquest.io/blog/web-scraping-tutorial-python/


# Documentacion que puede ser util
# https://2.python-requests.org//en/master/user/quickstart/#response-content

import requests
from bs4 import BeautifulSoup

#%%
page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
#print (page.content)
soup = BeautifulSoup(page.content, 'html.parser')
#print (soup.prettify())
print ("primer nivel")
print (list(soup.children))
#out = [type(item) for item in list(soup.children)]
out = list(soup.children)[2]
#out = list(out.children)[]
print ("Segundo nivel")
print (out)