
from dataclasses import dataclass
import urllib.request
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import os
import re
from geotext import GeoText
from datetime import datetime

#


####################################################### NOT READY YET
# working on 

def scraper(url, date, access_time):

    # get html
    request = urllib.request.Request(url)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html,'html.parser')

    # find date_of_publication
    div = soup.find("div", class_="col last-reviewed")
    i = 1
    date_of_publication = ""
    for item in div:
        if (i > 2):
            break
        if (i == 2):
            date_of_publication += " "
        i+=1
        date_of_publication += " ".join(item.text.split())
    date_of_publication = date


    # find headline
    headline = soup.find("h1", id="content").text

    # # store main_text                   

    
    main_text = ""
    texts = soup.find_all("div", class_="card bg-transparent border-0 rounded-0 mb-3")
    i = 0
    for text in texts:
        if (i >= 3):
            break
        main_text += text.text
        main_text += "\n"
        i += 1

    #to get the current working directory
    directory = os.getcwd()
    json_file_name = directory + f"\PHASE_1\API_SourceCode\web_scrape\{headline}.json"

    extracted_records = {
                        'url':url,
                        'date_of_publication':date,
                        'headline':headline,
                        'main_text':main_text,
                        'reports':[]
                        }


    # save data into a JSON file
    with open(json_file_name, 'w') as outfile:
        json.dump(extracted_records, outfile, indent=4)


