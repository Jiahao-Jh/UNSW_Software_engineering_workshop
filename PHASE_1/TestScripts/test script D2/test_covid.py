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


def test_covid_country_date_US():
    request = api_url + "covid?" + "country=US" + "&date=02-02-2020"
    
    #need to change local time to UTC, then change format
    datetime_now = (datetime.now(timezone('UTC'))).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        if i == "access_time":
            response_time = response[i]
            response.pop(i)
            break
    
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == {
                        "team_name": "SENG3011_GroupName",
                        "url": "https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=covid_19_data.csv",
                        "Confirmed": 8,
                        "Recovered": 0,
                        "Deaths": 0
    }
    
    
    
def test_covid_country_date_Mainland_China():
    request = api_url + "covid?" + "country=Mainland_China" + "&date=02-02-2020"
    
    #need to change local time to UTC, then change format
    datetime_now = datetime.now(timezone('UTC')).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        if i == "access_time":
            response_time = response[i]
            response.pop(i)
            break
    
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == {
                        "team_name": "SENG3011_GroupName",
                        "url": "https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=covid_19_data.csv",
                        "Confirmed": 16607,
                        "Recovered": 463,
                        "Deaths": 361
    }
    
    
    
def test_covid_country_date_Australia():
    request = api_url + "covid?" + "country=Australia" + "&date=02-02-2020"
    
    #need to change local time to UTC, then change format
    datetime_now = datetime.now(timezone('UTC')).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        if i == "access_time":
            response_time = response[i]
            response.pop(i)
            break
    
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == {
                        "team_name": "SENG3011_GroupName",
                        "url": "https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=covid_19_data.csv",
                        "Confirmed": 12,
                        "Recovered": 2,
                        "Deaths": 0
    }
    
    
    
def test_covid_state_country_date_US():
    request = api_url + "covid?" + "state=Chicago,_IL" + "&country=US" + "&date=02-02-2020"
    
    #need to change local time to UTC, then change format
    datetime_now = datetime.now(timezone('UTC')).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        if i == "access_time":
            response_time = response[i]
            response.pop(i)
            break
    
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == {
                        "team_name": "SENG3011_GroupName",
                        "url": "https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=covid_19_data.csv",
                        "Confirmed": 2,
                        "Recovered": 0,
                        "Deaths": 0
    }



def test_covid_state_country_date_Mainland_China():
    request = api_url + "covid?" + "state=Shanghai" + "&country=Mainland_China" + "&date=02-02-2020"
    
    #need to change local time to UTC, then change format
    datetime_now = datetime.now(timezone('UTC')).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        if i == "access_time":
            response_time = response[i]
            response.pop(i)
            break
    
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == {
                        "team_name": "SENG3011_GroupName",
                        "url": "https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=covid_19_data.csv",
                        "Confirmed": 182,
                        "Recovered": 10,
                        "Deaths": 1
    }
    
    
    
def test_covid_state_country_date_Australia():
    request = api_url + "covid?" + "state=New_South_Wales" + "&country=Australia" + "&date=02-02-2020"
    
    #need to change local time to UTC, then change format
    datetime_now = datetime.now(timezone('UTC')).strftime("%m/%d/%Y, %H:%M:%S")
    
    response = make_json_request(request)
    
    #get the access time and then remove it
    for i in response:
        if i == "access_time":
            response_time = response[i]
            response.pop(i)
            break
    
    #check true or false of access_time by comparing the time difference which should be less than 5 seconds
    access_time_status = check_access_time(int(response_time[-2:]) - int(datetime_now[-2:]))
    
    #check access_time is ture or not
    assert True == access_time_status
    assert response == {
                        "team_name": "SENG3011_GroupName",
                        "url": "https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=covid_19_data.csv",
                        "Confirmed": 4,
                        "Recovered": 2,
                        "Deaths": 0
    }


        
def test_covid_state_date_US():
    request = api_url + "covid?" + "state=Chicago,_IL" + "&date=02-02-2020"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"

    

def test_covid_state_date_Mainland_China():
    request = api_url + "covid?" + "state=Shanghai" + "&date=02-02-2020"
    
    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
    
    
def test_covid_state_date_Australia():
    request = api_url + "covid?" + "state=New_South_Wales" + "&date=02-02-2020"
    
    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    

def test_covid_state_country_US():
    request = api_url + "covid?" + "state=Chicago,_IL" + "&&country=US"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"

    

def test_covid_state_country_Mainland_China():
    request = api_url + "covid?" + "state=Shanghai" + "&&country=Mainland_China"
    
    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
    
    
def test_covid_state_country_Australia():
    request = api_url + "covid?" + "state=New_South_Wales" + "&country=Australia"
    
    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
    
def test_covid_only_state():
    request = api_url + "covid?" + "state=Chicago,_IL"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"

    

def test_covid_only_country():
    request = api_url + "covid?" + "country=Mainland_China"
    
    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
    
    
def test_covid_only_date():
    request = api_url + "covid?" + "date=02-02-2020"
    
    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the number of parameters"
    
    
    
def test_covid_wrong_type_parameters():
    request = api_url + "covid?" + "state=123" + "&country=US" + "&date=02_02_2020"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the type of parameters"



def test_covid_wrong_value_parameters():
    request = api_url + "covid?" +  "&country=US" + "&date=2020-02-02"

    response = make_request(request)
    
    assert response.status_code == 400
    assert response.text == "Check the value of parameters"
    
    

def test_covid_content_not_found():
    request = api_url + "covid?" + "state=Chicago,_IL" + "&country=US" + "&date=02-02-2018"

    response = make_request(request)
    
    assert response.status_code == 204
    assert response.text == ""