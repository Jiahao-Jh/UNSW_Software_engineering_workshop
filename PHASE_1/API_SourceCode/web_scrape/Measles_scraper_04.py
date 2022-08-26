
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
    main_text = soup.find("div", class_="col-md-8").text

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
            "name": "Measles (Rubeola)"
        }
        disease_list.append(disease)


    # find event_date
    if (re.findall(r'MMWR.* \d\d,\d+', main_text) == []):
        event_date = date[10:]
    else:
        event_date = re.findall(r'MMWR.* \d\d,\d+', main_text)[0]
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
    elif (re.findall(r'\d+ measles cases', main_text) != []):
        cases = re.findall(r'\d+ measles cases', main_text)[1]
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
# url = "https://www.cdc.gov/measles/cases-outbreaks.html"
# main_text = "cdc updates this page monthly.\nmeasles cases in 2022\nas of march 3, 2022, a total of 2 measles cases were reported by 2 jurisdictions. *\nmeasles cases in 2021\nfrom january 1 to december 31, 2021, a total of 49 measles cases were reported by 5 jurisdictions. *\nmeasles cases in 2020\nfrom january 1 to december 31, 2020, 13 individual cases of measles were confirmed in 8 jurisdictions.*\n*jurisdictions refer to any of the 50 states, new york city, and the district of columbia.\nmeasles cases in 2019\n\nfrom january 1 to december 31, 2019, 1,282* individual cases of measles were confirmed in 31 states.\nthis is the greatest number of cases reported in the u.s. since 1992. the majority of cases were among people who were not vaccinated against measles. measles is more likely to spread and cause outbreaks in u.s. communities where groups of people are unvaccinated.\nfor more information please see the following reports:\n\nincrease in measles cases \u2013 united states, january 1-april 26, 2019 mmwr. may 3, 2019\nnational update on measles cases and outbreaks \u2013 united states, january 1-october 1, 2019. mmwr. october 11, 2019\n\n\n\n"

# scraper(url, "ANNOUNCED JANUARY 2020", current_time)
