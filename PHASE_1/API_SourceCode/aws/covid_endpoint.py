from json import dumps
from dateutil.parser import parse
from dataset import parse_dataset
from datetime import datetime

def error(code, message):
    response = {}
    response["statusCode"] = code
    response["headers"]={}
    response["headers"]['Content-Type']= 'application/json'
    response["body"] = message
    return response

def lambda_handler(event, context):
    if 'country' not in event['queryStringParameters']:
        return error(400, "Check the number of parameters")  
    if 'date' not in event['queryStringParameters']:
        return error(400, "Check the number of parameters")  
    
    access_time = datetime.now()
    
    location = ''
    if 'state' in event['queryStringParameters']:  
        location = event['queryStringParameters']['state']
        location = location.replace("_"," ")

    country = event['queryStringParameters']['country']
    country = ' '.join(country.split("_"))
    
    date = event['queryStringParameters']['date']
    

    try:
        parse(date, dayfirst=True) 
        date = date.replace("-","/")
        tmp = date.split("/")
        tmp[0] , tmp[1] = tmp[1] , tmp[0]
        date = "/".join(tmp)
    except:
        return error(400, "Check the type of parameters")
    
    try:
        res = parse_dataset(location, country, date)
    except:
        return error(400, "Check the value of parameters")    
    
    if res == -1:
        return error(204,  "Content Not Found")  
    
    # finish_time = datetime.now()
    # print("Process time: "  ,finish_time - access_time)
    
    
    res["team_name"] = "SENG3011_GroupName"
    res["access_time"] = access_time.strftime("%m/%d/%Y, %H:%M:%S")
    res["url"] = "https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=covid_19_data.csv"
    
    response = {}
    response["statusCode"] = 200
    response["headers"]={}
    response["headers"]['Content-Type']= 'application/json'
    response["body"] = dumps(res)   
    
    
    return response