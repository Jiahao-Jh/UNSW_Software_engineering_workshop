from json import dumps
from datetime import datetime
from CDC_scraper import request

def error(code, message):
    response = {}
    response["statusCode"] = code
    response["headers"]={}
    response["headers"]['Content-Type']= 'application/json'
    response["body"] = message
    return response


def lambda_handler(event, context):
    if 'key_term' not in event['multiValueQueryStringParameters']:
        return error(400, "Check the number of parameters")  
      
    if 'location' not in event['queryStringParameters']:
        return error(400, "Check the number of parameters") 
      
    if 'period_of_interest' not in event['multiValueQueryStringParameters']:
        return error(400, "Check the number of parameters")  
    
    
     
    access_time = datetime.now()
    
    location = event['queryStringParameters']['location']
    location = location.replace("_"," ")
  
    key_term = event['multiValueQueryStringParameters']['key_term']
    
    for i in range(len(key_term)): 
        key_term[i] = key_term[i].replace("_"," ")
    
       
    period_of_interest = event['multiValueQueryStringParameters']['period_of_interest']  
    
    limit = 0
    try:
        if 'limit' in event['queryStringParameters']:  
            limit = int(event['queryStringParameters']['limit'])
    except:
        return error(400, "Check the value of parameters")  


    for i in range(len(key_term)):
        if i == 0:
            res = request(location, key_term[i], period_of_interest, limit)
        else:
            res = res.append(request(location, key_term[i], period_of_interest, limit))
        if res == 2:
            return error(400,  "Check the value of parameters, Incorrect date format")
        if res == 400:
            return error(400,  "Check the value of parameters")
        if res == 204:
            return error(204,  "Content Not Found")    
    
    
    for i in range(len(res)): 
        res[i]["team_name"] = "SENG3011_GroupName"
        res[i]["access_time"] = access_time.strftime("%m/%d/%Y, %H:%M:%S")
    
    response = {}
    response["statusCode"] = 200
    response["headers"]={}
    response["headers"]['Content-Type']= 'application/json'
    response["body"] = dumps(res)   
    
    
    return response