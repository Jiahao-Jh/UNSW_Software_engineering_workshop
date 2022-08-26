
from dataclasses import dataclass
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
# https://www.cdc.gov/brucellosis/exposure/unpasteurized-dairy-products.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fbrucellosis%2Fexposure%2Fdrug-resistant-brucellosis-linked-raw-milk.html

def scraper(url, date, access_time):

    # get html
    url = "https://www.cdc.gov/brucellosis/exposure/unpasteurized-dairy-products.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fbrucellosis%2Fexposure%2Fdrug-resistant-brucellosis-linked-raw-milk.html"
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
    main_text = soup.find("div", class_="col-md-12").text

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
    if (soup.find("div", class_="display-6 text-white fw-500 pt-1 pb-1").text.strip('\n') != None):

        disease_list = []
        disease = {
            "name": soup.find("div", class_="display-6 text-white fw-500 pt-1 pb-1").text.strip('\n')
        }
        disease_list.append(disease)
    else:
        disease_list = []
        disease = {
            "name": "Risks from Unpasteurized Dairy Products"
        }
        disease_list.append(disease)


    # find event_date
    if (re.findall(r'As of .* \d,\d+', main_text) == []):
        event_date = date[10:]
    else:
        event_date = re.findall(r'As of .* \d,\d+', main_text)[0]
        if (len(event_date) < 6):
            event_date = date[10:]
        else:
            event_date = event_date[6:]


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
        location_list.append(location)

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
    if (re.findall(r'\d+ hospitaliz', main_text) != []):
            hospitalizations = re.findall(r'\d+ hospitaliz', main_text)[0]
            hospitalizations = int(re.findall(r'\d+', hospitalizations)[0])
    else:
        hospitalizations = 0

    if (re.findall(r'\d+ death', main_text) != []):
            deaths = re.findall(r'\d+ death', main_text)[0]
            deaths = int(re.findall(r'\d+', deaths)[0])
    else:
        deaths = 0
    
    if (re.findall(r'\d+ cases', main_text) != []):
        cases = re.findall(r'\d+ cases', main_text)[0]
        cases = int(re.findall(r'\d+', cases)[0])
    else:
        if (hospitalizations != 0):
            cases = hospitalizations
        elif (deaths != 0):
            cases = deaths
        elif (hospitalizations != 0 and deaths != 0):
            cases = hospitalizations
        else:
            cases = 0


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
# url = "https://www.cdc.gov/brucellosis/exposure/unpasteurized-dairy-products.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fbrucellosis%2Fexposure%2Fdrug-resistant-brucellosis-linked-raw-milk.html"
# main_text = "Raw milk and milk products are those that have not undergone a process called pasteurization that kills disease-causing germs. These types of products are common outside the United States and are increasingly being sold in mainstream supermarkets in the United States as well.\nConsumption of raw milk containing Brucella can cause brucellosis. Most cases of brucellosis associated with raw milk are caused by a strain called Brucella melitensis or Brucella abortus in people who traveled to countries where these strains are\u00a0 common and drank contaminated cow, sheep or goat milk. In rare cases, brucellosis cases associated with other strains, including RB51 and Brucella suis, are reported.\nRB51 is resistant to certain antibiotics that would normally be used to prevent or treat Brucella infections. CDC recommends that anyone exposed to RB51 receive antibiotics to prevent an infection.\nTreatment recommendations: Exposure to RB51 through Raw Milk or Milk Products: How to Reduce Risk of Infection.\nRelated Links\nRaw Milk Questions and Answers\nTravelers\u2019 Health \u2013 Brucellosis\n\n"

# scraper(url, "ANNOUNCED JANUARY 2020", current_time)
