

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
# https://www.cdc.gov//measles/cases-outbreaks.html
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
            "name": "Viral Hepatitis"
        }
        disease_list.append(disease)


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
                    "location" : "America"
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

    details = soup.find("div", class_="card bt-3 bt-amber-s mb-3").text.split("\n")

    # find event date
    event_date = re.findall(r'\d+',details[0])[0]

    # find cases, hospitalizations and deaths
    cases = re.findall(r'\d+,\d+',details[2])[0]
    cases = int(re.sub(',', '', cases))

    hospitalizations = re.findall(r'\d+,\d+',details[3])[0]
    hospitalizations = int(re.sub(',', '', hospitalizations))

    deaths = int(re.findall(r'\d+',details[4])[0])


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
# url = "https://www.cdc.gov/hepatitis/outbreaks/2017March-HepatitisA.htm"
# main_text = "when hearing about hepatitis a, many people think about contaminated food and water. however, in the united states, hepatitis a is more commonly spread from person to person. since march 2017, cdc\u2019s division of viral hepatitis (dvh) has been assisting multiple state and local health departments with hepatitis a outbreaks, spread through person-to-person contact.\nthe hepatitis a vaccine is the best way to prevent hepatitis a virus (hav) infection \n\nthe following groups are at highest risk for acquiring hav infection or developing serious complications from hav infection in these outbreaks and should be offered the hepatitis a vaccine in order to prevent or control an outbreak:\n\npeople who use drugs (injection or non-injection)\npeople experiencing unstable housing or homelessness \nmen who have sex with men (msm)\npeople who are currently or were recently incarcerated \npeople with chronic liver disease, including cirrhosis, hepatitis b, or hepatitis c\n\n\none dose of single-antigen hepatitis a vaccine has been shown to control outbreaks of hepatitis a.1,2\npre-vaccination serologic testing is not required to administer hepatitis a vaccine.\u00a0vaccinations should not be postponed if vaccination history cannot be obtained or records are unavailable.\n\ncdc has provided outbreak-specific considerations for hepatitis a vaccine administration\u00a0and has updated its overall recommendations on the prevention of hepatitis a virus infection in the united states.\n\ncdc\u2019s response\nin response to all hepatitis outbreaks, cdc provides ongoing epidemiology and laboratory support as well as support on vaccine supply and vaccine policy development. when requested, cdc sends \u201cdisease detectives\u201d to affected areas to evaluate and assist in an outbreak response. cdc alerts other public health jurisdictions of any increases in disease. all jurisdictions are encouraged to be watchful for increases in hepatitis a cases. cdc also works with state and local health officials to ensure hepatitis a vaccine is targeted to the correct at-risk populations and that supply is adequate.\n\neducational resourcescdc is developing educational materials to support the outbreak at the state and local levels. most materials include an area where local information can be inserted. your organization\u2019s contact information can be typed into the blue colored rectangle. to upload your logo, click on the white space below the blue colored rectangle. in the pop-up box, select browse and upload a pdf version of your logo.\n\n"

# scraper(url, "ANNOUNCED JANUARY 2020", current_time)
