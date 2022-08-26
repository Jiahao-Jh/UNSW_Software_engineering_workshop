from multiprocessing.spawn import prepare
import pytest

from urllib import request, response
import requests
import time
from datetime import date
from datetime import timedelta
from datetime import datetime
from pytz import timezone
import json


api_url = "https://9qa0etj35i.execute-api.ap-southeast-2.amazonaws.com/GroupNameAPI/v1.0/"

def make_json_request(request):
    data = requests.get(request)
    return data.json()

def make_request(request):
    data = requests.get(request)
    return data

#check true or false of access_time by comparing the time difference which should be less than 60 seconds due to the time used by scraper
def check_access_time(difference):
    if abs(difference) < 60:
        return True
    else:
        return False


def test_index_ebola():
    request = api_url + "index?" + "location=Beni" + "&key_term=ebola" + "&period_of_interest=17-03-17T20:33:40&period_of_interest=22-04-18T21:23:52"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone("UTC"))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == "access_time":
                response_time = i[j]
                i.pop(j)
                break
    
    f = open("input_file_main_text_index.json")
    data = json.load(f)
    main_text = data["main_text"]
    f.close()
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    res = [
                        {
                            "url": "https://www.cdc.gov/vhf/ebola/", 
                            "date_of_publication": "Not applicable", 
                            "headline": "Ebola (Ebola Virus Disease) | CDC", 
                            "main_text": main_text["Ebola"], 
                            "reports": 
                                [{
                                    "disease": "ebola", 
                                    "syndromes": "Not implemented yet", 
                                    "locations": [{"country": "", "city": "Beni"}, 
                                                 {"country": "", "city": "Goma"}],
                                    "event_date": "December 16 2021", 
                                    "cases": "Not specified", 
                                    "death": "Not specified", 
                                    "hospitalization": "Not specified"
                                }, 
                                {
                                    "disease": "ebola", 
                                    "syndromes": "Not implemented yet", 
                                    "locations": [{"country": "", "city": "Beni"}, 
                                                 {"country": "", "city": "Goma"}], 
                                    "event_date": "December 16 2021", 
                                    "cases": "Not specified", 
                                    "death": "Not specified", 
                                    "hospitalization": "Not specified"
                                }
                                ], 
                                "team_name": "SENG3011_GroupName"
                                }]
    
    response =  sorted(response, key=lambda d: d['main_text']) 
    res = sorted(res, key=lambda d: d['main_text']) 
    
       
    for i in range(len(response)):
        if response[i]['reports'] != []:
            for x in range(len(response[i]['reports'])):
                response[i]['reports'][x]["locations"] = sorted(response[i]['reports'][x]["locations"], key=lambda d: d['city'])
        
    for i in range(len(res)):
        if res[i]['reports'] != []:
            for x in range(len(res[i]['reports'])):
                res[i]['reports'][x]["locations"] = sorted(res[i]['reports'][x]["locations"], key=lambda d: d['city'])
    #check access_time is ture or not
    assert True == access_time_status
    assert response == res 
    
    
    
def test_index_Salmonella():
    request = api_url + "index?" + "location=Bareilly" + "&key_term=salmonella" + "&period_of_interest=20-03-17T20:33:40&period_of_interest=20-04-18T21:23:52"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone("UTC"))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == "access_time":
                response_time = i[j]
                i.pop(j)
                break
    
    f = open("input_file_main_text_index.json")
    data = json.load(f)
    main_text = data["main_text"]
    f.close()
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    res = [
             {
                 "url": "https://www.cdc.gov/healthypets/diseases/salmonella.html", 
                 "date_of_publication": "Not applicable", 
                 "headline": "Salmonella Infection | Healthy Pets, Healthy People | CDC", 
                 "main_text": main_text["Salmonella_Infection"], 
                 "reports": [], 
                 "team_name": "SENG3011_GroupName"
             },
             {
                 "url": "https://www.cdc.gov/typhoid-fever/index.html", 
                 "date_of_publication": "Not applicable", 
                 "headline": "Home | Typhoid Fever | CDC", 
                 "main_text": main_text["Typhoid_Fever"], 
                 "reports": [], 
                 "team_name": "SENG3011_GroupName"
             },
             {
                 "url": "https://www.cdc.gov/salmonella", 
                 "date_of_publication": "Not applicable", 
                 "headline": "Salmonella Homepage | CDC", 
                 "main_text": main_text["Salmonella_homepage"], 
                 "reports": [{
                     "disease": "Salmonella", 
                     "syndromes": "Not implemented yet", 
                     "locations": [{"country": "", "city": "Altona"}, 
                                     {"country": "", "city": "Bareilly"}, 
                                     {"country": "", "city": "Hartford"},
                                     {"country": "", "city": "New York"}], 
                     "event_date": "April 12, 2020, to November 24, 2020", 
                     "cases": 49, 
                     "death": 0, 
                     "hospitalization": 0}], 
                 "team_name": "SENG3011_GroupName"
             }
             ]
    
    response =  sorted(response, key=lambda d: d['main_text']) 
    res = sorted(res, key=lambda d: d['main_text']) 
    
       
    for i in range(len(response)):
        if response[i]['reports'] != []:
            for x in range(len(response[i]['reports'])):
                response[i]['reports'][x]["locations"] = sorted(response[i]['reports'][x]["locations"], key=lambda d: d['city'])
        
    for i in range(len(res)):
        if res[i]['reports'] != []:
            for x in range(len(res[i]['reports'])):
                res[i]['reports'][x]["locations"] = sorted(res[i]['reports'][x]["locations"], key=lambda d: d['city'])
    #check access_time is ture or not
    assert True == access_time_status
    assert response == res
    
    

def test_index_Measles():
    request = api_url + "index?location=Florida&key_term=measles&period_of_interest=00-03-17T20:33:40&period_of_interest=22-04-18T21:23:52"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone("UTC"))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == "access_time":
                response_time = i[j]
                i.pop(j)
                break
    
    f = open("input_file_main_text_index.json")
    data = json.load(f)
    main_text = data["main_text"]
    
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    res = [
                        {
                            "url": "https://www.cdc.gov/vaccinesafety/vaccines/mmrv-vaccine.html", 
                            "date_of_publication": "Not applicable", 
                            "headline": "Safety Information for Measles, Mumps, Rubella, Varicella Vaccines | CDC", 
                            "main_text": "Measles\xa0causes fever" + main_text["Safety_Measles"], 
                            "reports": [], 
                            "team_name": "SENG3011_GroupName"
                        }, 
                        {
                            "url": "https://www.cdc.gov/measles/vaccination.html", 
                            "date_of_publication": "Not applicable", 
                            "headline": "Vaccine for Measles (MMR Shot) | CDC", 
                            "main_text": main_text["Vaccine_Measles"], 
                            "reports": [{
                                "disease": "measles", 
                                "syndromes": "Not implemented yet", 
                                "locations": [{"country": "","city": "New York"},
                                             {"country": "","city": "Missouri"},
                                             {"country": "","city": "Griffith"},
                                             {"country": "","city": "Asia"},
                                             {"country": "","city": "Oklahoma"},
                                             {"country": "","city": "Iowa"},
                                             {"country": "","city": "Michigan"},
                                             {"country": "","city": "Colorado"},
                                             {"country": "","city": "Washington"},
                                             {"country": "","city": "Florida"},
                                             {"country": "","city": "Atlanta"},
                                             {"country": "","city": "Oregon"},
                                             {"country": "","city": "Clemmons"},
                                             {"country": "","city": "Texas"},
                                             {"country": "","city": "McLean"},
                                             {"country": "","city": "Rota"},
                                             {"country": "","city": "Maryland"},
                                             {"country": "","city": "Virginia"}], 
                                "event_date": "October 11 2019", 
                                "cases": -1, 
                                "death": -1, 
                                "hospitalization": -1}], 
                            "team_name": "SENG3011_GroupName"
                        }, 
                        {
                            "url": "https://www.cdc.gov/measles/index.html", 
                            "date_of_publication": "Not applicable",
                            "headline": "Measles (Rubeola) | CDC", 
                            "main_text": "Prevent Measles", 
                            "reports": [{
                                "disease": "measles", 
                                "syndromes": "Not implemented yet", 
                                "locations": [
                                            {"country": "","city": "New York"},
                                            {"country": "","city": "Missouri"},
                                            {"country": "","city": "Griffith"},
                                            {"country": "","city": "Asia"},
                                            {"country": "","city": "Oklahoma"},
                                            {"country": "","city": "Iowa"},
                                            {"country": "","city": "Michigan"},
                                            {"country": "","city": "Colorado"},
                                            {"country": "","city": "Washington"},
                                            {"country": "","city": "Florida"},
                                            {"country": "","city": "Atlanta"},
                                            {"country": "","city": "Oregon"},
                                            {"country": "","city": "Clemmons"},
                                            {"country": "","city": "Texas"},
                                            {"country": "","city": "McLean"},
                                            {"country": "","city": "Rota"},
                                            {"country": "","city": "Maryland"},
                                            {"country": "","city": "Virginia"}], 
                                "event_date": "October 11 2019", 
                                "cases": -1, 
                                "death": -1, 
                                "hospitalization": -1
                                }], 
                            "team_name": "SENG3011_GroupName"
                            }
                            ]
    
    
    response =  sorted(response, key=lambda d: d['main_text']) 
    res = sorted(res, key=lambda d: d['main_text']) 
    
       
    for i in range(len(response)):
        if response[i]['reports'] != []:
            for x in range(len(response[i]['reports'])):
                response[i]['reports'][x]["locations"] = sorted(response[i]['reports'][x]["locations"], key=lambda d: d['city'])
        
    for i in range(len(res)):
        if res[i]['reports'] != []:
            for x in range(len(res[i]['reports'])):
                res[i]['reports'][x]["locations"] = sorted(res[i]['reports'][x]["locations"], key=lambda d: d['city'])
    #check access_time is ture or not
    assert True == access_time_status
    assert response == res



def test_index_Hantavirus():
    request = api_url + "index?" + "location=all" + "&key_term=hantavirus" + "&period_of_interest=10-03-17T20:33:40&period_of_interest=21-04-18T21:23:52"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone("UTC"))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == "access_time":
                response_time = i[j]
                i.pop(j)
                break
    
    f = open("input_file_main_text_index.json")
    data = json.load(f)
    main_text = data["main_text"]
    
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == [
                        {
                            "url": "https://www.cdc.gov/hantavirus/", 
                            "date_of_publication": "Not applicable", 
                            "headline": "CDC - Hantavirus", 
                            "main_text": main_text["Hantavirus_part_1"] + "\xa0" + main_text["Hantavirus_part_2"] + "“New World”" + main_text["Hantavirus_part_3"] + "“Old World”" + main_text["Hantavirus_part_4"], 
                            "reports": 
                                [{
                                    "disease": "hantavirus", 
                                    "syndromes": "Not implemented yet", 
                                    "locations": [], 
                                    "event_date": "January 2017 ", 
                                    "cases": -1, 
                                    "death": -1, 
                                    "hospitalization": -1
                                }, 
                                {"disease": "hantavirus", 
                                 "syndromes": "Not implemented yet", 
                                 "locations": [], 
                                 "event_date": "August 2012", 
                                 "cases": -1, 
                                 "death": -1, 
                                 "hospitalization": -1
                                 }], "team_name": "SENG3011_GroupName"}]



def test_index_no_report():
    request = api_url + "index?" + "location=Beni" + "&key_term=ebola" + "&period_of_interest=00-03-17T20:33:40&period_of_interest=01-04-18T21:23:52"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone("UTC"))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == "access_time":
                response_time = i[j]
                i.pop(j)
                break
    
    f = open("input_file_main_text_index.json")
    data = json.load(f)
    main_text = data["main_text"]
    f.close()
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == [
                        {
                            "url": "https://www.cdc.gov/vhf/ebola/", 
                            "date_of_publication": "Not applicable", 
                            "headline": "Ebola (Ebola Virus Disease) | CDC", 
                            "main_text": main_text["Ebola"], 
                            "reports": [],
                            "team_name": "SENG3011_GroupName"
                        }]
    
    
    
def test_index_with_less_parameter_period():
    request = api_url + "index?" + "location=Beni" + "&key_term=ebola"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
def test_index_with_less_parameter_loaction():
    request = api_url + "index?" + "key_term=ebola" + "&period_of_interest=00-03-17T20:33:40&period_of_interest=22-04-18T21:23:52"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
def test_index_with_less_parameter_key_term():
    request = api_url + "index?" + "location=Beni" + "&period_of_interest=00-03-17T20:33:40&period_of_interest=22-04-18T21:23:52"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
def test_index_with_wrong_value():
    request = api_url + "index?" + "location=" + "&key_term=ebola" + "&period_of_interest=00-03-17T20:33:40&period_of_interest=22-04-18T21:23:52"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the value of parameters"
    
def test_index_with_wrong_value_period():
    request = api_url + "index?" + "location=Beni" + "&key_term=ebola" + "&period_of_interest=00-03-17S20:33:40&period_of_interest=22-04-18S21:23:52"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the value of parameters, Incorrect date format"

def test_index_with_wrong_url():
    request = api_url + "index?" + "location=123" + "&key_term=dsa" + "&period_of_interest=99-01-01T00:00:00&period_of_interest=99-01-01T00:00:01"

    response = make_request(request)
    
    assert response.status_code == 204
    assert response.text == ""

if __name__ == '__main__':
    test_index_Salmonella()