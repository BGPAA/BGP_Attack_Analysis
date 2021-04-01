import os
import pytz
import wget
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# Obtenir la date et heure d'il y a 5 minutes en timezone UTC
now = datetime.now(pytz.utc) - timedelta(minutes=5)
year = now.strftime("%Y")
month = now.strftime("%m")

url_source = 'http://data.ris.ripe.net/rrc21/'+year+'.'+month+'/'
ext = 'gz'

def listFD(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

url = listFD(url_source, ext)[1]
print(url)
output_directory = os.getcwd()+'/tabi-master/input/rrc21'
filename = wget.download(url, out=output_directory)

