import nltk
import requests
from bs4 import BeautifulSoup
 
req = requests.get('https://en.wikipedia.org/wiki/Python_(programming_language)')
soup = BeautifulSoup(req.text, "lxml")

print (soup)
