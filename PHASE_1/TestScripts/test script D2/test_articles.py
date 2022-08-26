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

#check true or false of access_time by comparing the time difference which should be less than 5 seconds
def check_access_time(difference):
    if abs(difference) < 5 or abs(difference) > 55:
        return True
    else:
        return False


def test_articles_measles():
    request = api_url + "articles?" + "location=New_York" + "&key_term=measles" + "&period_of_interest=15-10-01T08:45:10&period_of_interest=22-11-01T19:37:12" + "&limit=0"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone('UTC'))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == 'access_time':
                response_time = i[j]
                i.pop(j)
                break
    
    f = open('input_file_main_text_articles.json')
    data = json.load(f)
    main_text = data["main_text"]
    f.close()
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == [
                        {
                            "team_name": "SENG3011_GroupName",
                            "url": "https://www.cdc.gov//measles/cases-outbreaks.html",
                            "date_of_publication": "Announced January 2019",
                            "header": "Measles Cases and Outbreaks",
                            "main_text": main_text["measles"],
                            "reports": [
                            {
                                "event_date": "January 2019",
                                "locations": [
                                {
                                    "country": "Have not been implantment",
                                    "location": "New York"
                                },
                                {
                                    "country": "Have not been implantment",
                                    "location": "Columbia"
                                }],
                                "diseases": 
                                    [{"name": "Measles (Rubeola)"}],
                                "syndromes": 
                                    [{"name": "did not find any"}],
                                "cases": 49,
                                "deaths": 0,
                                "hospitalizations": 0
                            }
                            ]
                        }
                       ]
    
    
    
def test_articles_lung_injury():
    request = api_url + "articles?" + "location=Columbia" + "&key_term=lung_injury" + "&period_of_interest=00-10-01T08:45:10&period_of_interest=22-11-01T19:37:12" + "&limit=0"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone('UTC'))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == 'access_time':
                response_time = i[j]
                i.pop(j)
                break
    
    f = open('input_file_main_text_articles.json')
    data = json.load(f)
    main_text = data["main_text"]
    f.close()
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == [
                        {
                            "team_name": "SENG3011_GroupName",
                            "url": "https://www.cdc.gov/tobacco/basic_information/e-cigarettes/severe-lung-disease.html",
                            "date_of_publication": "Announced August 2019",
                            "header": "Outbreak of Lung Injury Associated with the Use of E-Cigarette, or Vaping, Products",
                            "main_text": main_text["lung_injury"],
                            "reports": [
                            {
                                "event_date": "August 2019",
                                "locations": [
                                {
                                    "country": "Have not been implantment",
                                    "location": "Columbia"
                                }],
                                "diseases": 
                                    [{"name": "Smoking & Tobacco Use"}],
                                "syndromes": 
                                    [{"name": "did not find any"}],
                                "cases": 807,
                                "deaths": 0,
                                "hospitalizations": 807
                            }
                            ]
                        }
                        ]
    
    

def test_articles_brucellosis():
    request = api_url + "articles?" + "location=no" + "&key_term=brucellosis" + "&period_of_interest=00-10-01T08:45:10&period_of_interest=22-11-01T19:37:12" + "&limit=0"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone('UTC'))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == 'access_time':
                response_time = i[j]
                i.pop(j)
                break
    
    f = open('input_file_main_text_articles.json')
    data = json.load(f)
    main_text = data["main_text"]
    f.close()
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == [
                        {
                            'team_name': 'SENG3011_GroupName', 
                            'url': 'https://www.cdc.gov/brucellosis/exposure/unpasteurized-dairy-products.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fbrucellosis%2Fexposure%2Fdrug-resistant-brucellosis-linked-raw-milk.html', 
                            'date_of_publication': 'Announced February 2019', 
                            'header': 'Risks from Unpasteurized Dairy Products', 
                            'main_text': main_text["brucellosis"],
                            'reports': 
                                [{
                                    'event_date': 'February 2019', 
                                    'locations': 
                                        [{
                                            'country': 'Have not been implantment', 
                                            'location': 'did not find any'
                                        }], 
                                    'diseases': 
                                        [{'name': 'Brucellosis'}], 
                                    'syndromes':
                                        [{'name': 'infection'}], 
                                    'cases': 0, 
                                    'deaths': 0, 
                                    'hospitalizations': 0
                                }]
                            }
                        ]
    
    
    
def test_articles_viral_hepatitis():
    request = api_url + "articles?" + "location=US" + "&key_term=viral_hepatitis" + "&period_of_interest=00-10-01T08:45:10&period_of_interest=22-11-01T19:37:12" + "&limit=0"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone('UTC'))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == 'access_time':
                response_time = i[j]
                i.pop(j)
                break
    
    f = open('input_file_main_text_articles.json')
    data = json.load(f)
    main_text = data["main_text"]
    f.close()
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == [
                        {
                            'team_name': 'SENG3011_GroupName', 
                            'url': 'https://www.cdc.gov/hepatitis/outbreaks/2017March-HepatitisA.htm', 
                            'date_of_publication': 'Announced March 2017', 
                            'header': 'Widespread person-to-person outbreaks of hepatitis A across the United States', 
                            'main_text': main_text["viral_hepatitis"], 
                            'reports': [{
                                'event_date': '2016', 
                                'locations': [{
                                    'country': 'Have not been implantment', 
                                    'location': 'America'
                                    }], 
                                'diseases': 
                                    [{'name': 'Viral Hepatitis'}], 
                                'syndromes': 
                                    [{'name': 'infection'}], 
                                'cases': 43906, 
                                'deaths': 419, 
                                'hospitalizations': 26798
                            }]
                        }]
    
    
    
    
def test_articles_Listeria():
    request = api_url + "articles?" + "location=US" + "&key_term=Listeria" + "&period_of_interest=00-10-01T08:45:10&period_of_interest=22-11-01T19:37:12" + "&limit=0"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone('UTC'))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        for j in i:
            print(j)
            if j == 'access_time':
                response_time = i[j]
                i.pop(j)
                break
    
    f = open('input_file_main_text_articles.json')
    data = json.load(f)
    main_text = data["main_text"]
    f.close()
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status 
    assert response == [
                        {
                            'team_name': 'SENG3011_GroupName', 
                            'url': 'https://www.cdc.gov/listeria/outbreaks/packaged-salad-mix-12-21/index.html', 
                            'date_of_publication': 'Announced December 2021', 
                            'header': 'Listeria Outbreak Linked to Packaged Salads Produced by Dole', 
                            'main_text': main_text["Listeria_Dole"], 
                            'reports': 
                                [{
                                    'event_date': '11/30/21', 
                                    'locations': 
                                        [{
                                            'country': 'Have not been implantment', 
                                            'location': 'Dole'
                                        }], 
                                    'diseases': 
                                        [{
                                            'name': 'Listeria (Listeriosis)'
                                        }], 
                                    'syndromes': 
                                        [{'name': 'headache'}, 
                                         {'name': 'fever'},
                                         {'name': 'diarrhea'}, 
                                         {'name': 'aches'}], 
                                    'cases': 17, 
                                    'deaths': 2, 
                                    'hospitalizations': 13
                                }]
                            }, 
                        {
                            'team_name': 'SENG3011_GroupName', 
                            'url': 'https://www.cdc.gov/listeria/outbreaks/packaged-salad-12-21-b/index.html', 
                            'date_of_publication': 'Announced December 2021', 
                            'header': 'Listeria Outbreak Linked to Packaged Salads Produced by Fresh Express', 
                            'main_text': main_text["Listeria_Fresh_Express"], 
                            'reports': 
                                [{
                                    'event_date': 'December 2021', 
                                    'locations': 
                                        [{
                                            'country': 'Have not been implantment', 
                                            'location': 'did not find any'
                                        }], 
                                    'diseases': 
                                        [{'name': 'Listeria (Listeriosis)'}], 
                                    'syndromes': 
                                        [{'name': 'did not find any'}], 
                                    'cases': 10, 
                                    'deaths': 1, 
                                    'hospitalizations': 10
                                }]
                        }
                        ]
    
def test_article_with_less_parameter_loaction():
    request = api_url + "articles?" + "&key_term=Listeria" + "&period_of_interest=00-10-01T08:45:10&period_of_interest=22-11-01T19:37:12" + "&limit=0"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
def test_article_with_less_parameter_key_term():
    request = api_url + "articles?" + "location=US" + "&period_of_interest=00-10-01T08:45:10&period_of_interest=22-11-01T19:37:12" + "&limit=0"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
def test_article_with_less_parameter_period():
    request = api_url + "articles?" + "location=US" + "&key_term=Listeria" + "&limit=0"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
def test_article_with_wrong_value_limit():
    request = api_url + "articles?" + "location=US" + "&key_term=Listeria" + "&period_of_interest=00-10-01T08:45:10&period_of_interest=22-11-01T19:37:12" + "&limit=abc"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the value of parameters"
    
def test_article_with_wrong_url():
    request = api_url + "articles?" + "location=africa" + "&key_term=Listeria" + "&period_of_interest=00-10-01T08:45:10&period_of_interest=22-11-01T19:37:12" + "&limit=1"

    response = make_request(request)
    
    assert response.status_code == 204
    assert response.text == ""