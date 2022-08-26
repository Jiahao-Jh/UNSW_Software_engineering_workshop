import urllib.request
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import os
import re
from geotext import GeoText
from datetime import datetime

# {
# url: <string>,
# date_of_publication: <string::date>,
# headline: <string>,
# main_text: <string>,
# reports: [<object::report>]
# }

# working on 
# https://www.cdc.gov/listeria/outbreaks/packaged-salad-mix-12-21/index.html
# https://www.cdc.gov/listeria/outbreaks/packaged-salad-12-21-b/index.html

def scraper(url, date, access_time):

    # get html
    request = urllib.request.Request(url)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html,'html.parser')

    # find date_of_publication
    # date_of_publication = soup.find("div", class_="card-body p-0 bg-transparent").p.text
    date_of_publication = date

    # find headline
    headline = soup.find("h1", id="content").text


    # store main_text                   
    all_text = soup.find_all("div", class_="card bt-3 bt-primary border-0 rounded-0 mb-3")
    main_text = ""
    x = 1
    for text in all_text:
        if (x != 1):
            main_text += "\n"
        main_text += text.text  
        x += 1

    # create report
    report_list = report(url, main_text, date)

    #to get the current working directory
    directory = os.getcwd()
    json_file_name = directory + f"\PHASE_1\API_SourceCode\web_scrape\json_data\{headline}.json"

    # store all the data
    extracted_records = {
                            "team_name": "SENG3011_GroupName",
                            "access_time": access_time,
                            "url": url,
                            "date_of_publication": date_of_publication,
                            "header": headline,
                            "main_text": main_text,
                            "reports": report_list
                        }

    # save data into a JSON file
    with open(json_file_name, 'w') as outfile:
        json.dump(extracted_records, outfile, indent=4)



def report(url, main_text, date):
    
    # get html
    request = urllib.request.Request(url)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html,'html.parser')

    # get disease name
    disease_list = []
    disease = {
        "name": soup.find("div", class_="display-6 text-white fw-500 pt-1 pb-1").text.strip('\n')
    }
    disease_list.append(disease)


    # find event_date
    if (re.findall(r'from \d+/\d+/\d+', main_text) == []):
        event_date = date[10:]
    else:
        event_date = re.findall(r'from \d+/\d+/\d+', main_text)[0]
        if (len(event_date) < 6):
            event_date = date[10:]
        else:
            event_date = event_date[5:]


    # find location
    location_list = []
    if (GeoText(main_text).cities == []):

        location = {
                    "country" : "Have not been implantment",
                    "location" : "did not find any"
                    }
        location_list.append(location)
    else:
        for city in GeoText(main_text).cities:
            # ignore special cases
            if (location_cases_ignore(city)):
                location = {
                            "country" : "Have not been implantment",
                            "location" : city
                            }
                if (location_list == []):
                    location_list.append(location)
                
                # check for duplicate
                else:
                    already_exist = 0
                    for loc in location_list:
                        if (loc == location):
                            already_exist = 1
                    if (not already_exist):
                        location_list.append(location)
                
    if (location_list == []):
        location = {
                "country" : "Have not been implantment",
                "location" : "did not find any"
                }

    # find syndromes
    my_syndromes = ["headache", "fever", "cold", "diarrhea", "sweating", "trance", "pain", "aches", 
                    "fainting", "bleeding", "cough", "vomiting", "hallucinations", "nervousness", 
                    "Haemorrhagic", "Paralysis", "gastroenteritis", "respiratory", "Influenza", 
                    "rash", "Encephalitis", "Meningitis", "infection"]

    syndromes_list = []

    for syndrome in my_syndromes:
        if (syndrome in main_text.lower()):
            syn = {
                "name" : syndrome
            }
            syndromes_list.append(syn)

    if (syndromes_list == []):
        syn = {
                "name" : "did not find any"
        }
        syndromes_list.append(syn)
    
 
    # find cases, deaths, hospitalization
    details = soup.find("div", class_="card-body bg-tertiary").text.split("\n")
    
    i = 0
    cases = 0
    deaths = 0
    hospitalizations = 0
    for detail in details:
     
        if (i == 1):
            cases = int(re.findall(r'\d+', detail)[0])
        elif (i == 2):
            hospitalizations = int(re.findall(r'\d+', detail)[0])
        elif (i == 3):
            deaths = int(re.findall(r'\d+', detail)[0])
        i += 1

    report = {    
                "event_date": event_date,
                "locations": location_list,
                "diseases": disease_list,
                "syndromes": syndromes_list,
                "cases": cases,
                "deaths": deaths,
                "hospitalizations": hospitalizations
            }

    report_list = []
    report_list.append(report)

    return report_list

# ignore special cases
def location_cases_ignore(location):
    location_cases_ignore = ['Bar', 'Best', 'Most', 'March']
    for ignore in location_cases_ignore:
        if (ignore == location):
            return 0
    return 1


# now = datetime.now()
# current_time = now.strftime("%d/%m/%Y %H:%M:%S")
# url = "https://www.cdc.gov/listeria/outbreaks/packaged-salad-12-21-b/index.html"
# main_text = "what you should doprevent listeria\n\nfind out if you are at higher risk for getting sick with listeria\nlearn which foods are more likely to contain listeria, and take steps to prevent getting sick\nstay up to date on food recalls and outbreaks to avoid getting sick from eating contaminated food\n\nprepare leafy greens safely\nvegetables, including leafy greens, are an important part of a healthy and balanced diet. however, they can sometimes be contaminated with harmful germs.\nthe safest produce is cooked; the next safest is washed. however, no washing method can remove all germs.\nwhen eating raw leafy greens:\n\nwash your hands, utensils, and surfaces before and after preparing leafy greens.\nclean leafy greens before eating or cutting them.\n\ndiscard outer leaves on whole heads of lettuce and any torn or bruised leaves.\nrinse under running water and use your hands to gently rub the surface of the leaves.\ndry with a clean cloth or paper towel.\nif the label on a leafy greens package says \u201cready to eat,\u201d \u201ctriple washed,\u201d or \u201cno washing necessary,\u201d you don\u2019t need to wash the greens.\n\n\nseparate leafy greens from raw meat, poultry, and seafood.\nrefrigerate leafy greens within 2 hours. refrigerate within 1 hour if they have been exposed to temperatures above 90\u00b0f (such as a hot car or picnic).\n\n"

# scraper(url, "ANNOUNCED JANUARY 2020", current_time)
