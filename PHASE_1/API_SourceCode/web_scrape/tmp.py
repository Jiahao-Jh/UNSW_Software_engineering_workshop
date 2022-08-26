
from datetime import datetime
from turtle import st
import os
import json
import sys
import urllib.request
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import re
from geotext import GeoText
url = "https://www.cdc.gov/hepatitis/outbreaks/2017March-HepatitisA.htm"
# get html

request = urllib.request.Request(url)
html = urllib.request.urlopen(request).read()
soup = BeautifulSoup(html,'html.parser')
details = soup.find("div", class_="card bt-3 bt-amber-s mb-3").text.split("\n")


event_date = re.findall(r'\d+',details[0])[0]
print(event_date)

cases = re.findall(r'\d+,\d+',details[2])[0]
cases = int(re.sub(',', '', cases))
print(cases)

hospitalizations = re.findall(r'\d+,\d+',details[3])[0]
hospitalizations = int(re.sub(',', '', hospitalizations))
print(hospitalizations)
deaths = int(re.findall(r'\d+',details[4])[0])
print(deaths)





