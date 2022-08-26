import urllib.request
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import os
from datetime import datetime

# different scraper for different articals
import Salads_scraper_01
import Lung_injury__scraper_02
import Raw_milk_scraper_03
import Measles_scraper_04
import hepatitis_A_scraper_05

json_file_location = os.environ['LAMBDA_TASK_ROOT'] + "/json_data"

def outbreak_links(access_time):
    url = "https://www.cdc.gov/outbreaks/"
    request = urllib.request.Request(url)
    html = urllib.request.urlopen(request).read()

    soup = BeautifulSoup(html,'html.parser')
    main_table = soup.find("ul",attrs={'class':'list-bullet feed-item-list'})
    links = main_table.find_all("a",class_="feed-item-title")
    dates = main_table.find_all("span")

    def is_absolute(url):
        return bool(urlparse(url).netloc)

    extracted_records = []
    i = 0

    # check if json data exists
    directory = os.getcwd()
    json_directory = directory + f"\PHASE_1\API_SourceCode\web_scrape\json_data"
    isExist = os.path.exists(json_directory)
    if (not isExist):
        os.makedirs(json_directory)
    
    for link in links: 
        title = link.text

        url = link['href']
        
        if not is_absolute(url):
            # use urljoin to join url
            url = "https://www.cdc.gov/" + url

        record = {
        'title':title,
        'url':url,
        'date':dates[i].text
        }
        extracted_records.append(record)

        # scrape all links
        if (i == 0 or i == 1):
            Salads_scraper_01.scraper(url, dates[i].text, access_time)
        elif (i == 3):
            Lung_injury__scraper_02.scraper(url, dates[i].text, access_time)
        elif (i == 4):
            Raw_milk_scraper_03.scraper(url, dates[i].text, access_time)
        elif (i == 5):
            Measles_scraper_04.scraper(url, dates[i].text, access_time)
        elif (i == 6):
            hepatitis_A_scraper_05.scraper(url, dates[i].text, access_time)
        i += 1
    


def find_artical_location(location):
    matched_location_artical_title = []

    # get each web data and try to find location
    json_dir = json_file_location
    for filename in os.listdir(json_dir):

        f = open(f"{json_dir}/{filename}")
        artical = json.load(f)
        
        if (location in artical['main_text'].lower() or location in artical['header'].lower()):
            matched_location_artical_title.append(artical["header"])

    return matched_location_artical_title



def find_artical_key_term(key_terms, available_articles):
    matched_key_terms_artical_title = []
    # if no articals available
    if (available_articles == []):
        return matched_key_terms_artical_title

    for artical_headline in available_articles:

        # get each web data and try to find location
        json_dir = json_file_location
        for filename in os.listdir(json_dir):

            f = open(f"{json_dir}/{filename}")
            artical = json.load(f)
            if (artical_headline == artical["header"]):

                # try to find key_term in artical
                for key in key_terms:
                    if (key in artical['main_text'].lower() or key in artical['header'].lower()):
                        matched_key_terms_artical_title.append(artical["header"])
                        break

    return matched_key_terms_artical_title



def find_artical_time(period_of_interest, available_articles):
    start_date = datetime.strptime(period_of_interest[0], '%y-%m-%dT%H:%M:%S')
    end_date = datetime.strptime(period_of_interest[1], '%y-%m-%dT%H:%M:%S')
    #  ["2015-10-01T08:45:10","2015-11-01T19:37:12"]
    matched_key_terms_artical_title = []

    for artical_headline in available_articles:
        
            # get each web data and try to find location
            json_dir = json_file_location
            for filename in os.listdir(json_dir):

                f = open(f"{json_dir}/{filename}")
                artical = json.load(f)
                if (artical_headline == artical["header"]):
                    # convert time
                    publish_date = datetime.strptime(artical["date_of_publication"], 'Announced %B %Y')
                    # check if time is vaild
                    if (publish_date > start_date and publish_date < end_date):
                        matched_key_terms_artical_title.append(artical["header"])

    return matched_key_terms_artical_title



def request(location, key_terms, period_of_interest, limit):
    
    # error checking
    if (location == "" or key_terms == ""):
        print("do not give empty inputs for location or key_terms")
        return 400

    # check date format
    if (not check_date_format(period_of_interest[0])):
        print(f"Incorrect data format: {period_of_interest[0]}")
        print("correct formate is: yyyy-MM-ddTHH:mm:ss")
        return 2
    if (not check_date_format(period_of_interest[1])):
        print(f"Incorrect data format: {period_of_interest[1]}")
        print("correct formate is: yyyy-MM-ddTHH:mm:ss")
        return 2

    #check all characters in the location are alphabets
    if (not location.isalpha()):
        print("please check all characters in the location are alphabets")
        return 400



    # scrape all outbreak and store in json format
    # outbreak_links(access_time)

    location = location.lower()
    key_terms = key_terms.lower()
    key_terms = key_terms.split(",")

    
    matched_artical_title = find_artical_location(location)

    matched_artical_title = find_artical_key_term(key_terms, matched_artical_title)

    matched_artical_title = find_artical_time(period_of_interest, matched_artical_title)

    
    # check if limit required
    if (limit):
        # check if matched artical is greater than 5
        if (len(matched_artical_title) > limit):
            matched_artical_title = matched_artical_title[0:5]
        # check if matched artical list is empty
        elif (len(matched_artical_title) <= 0):
            return 204
    else:
        # check if matched artical list is empty
        if (len(matched_artical_title) <= 0):
            return 204

    # get each web data and try to find location
    json_dir = json_file_location
    res = []    
    for i in matched_artical_title: 
        i += ".json"
        with open(f"{json_dir}/{i}") as f:
            res.append(json.load(f))
                
    return res


# input a date, return true if format is correct
def check_date_format(date):

    format = "%y-%m-%dT%H:%M:%S"
    # checking if format matches the date
    res = True
    # using try-except to check for truth value
    try:
        res = bool(datetime.strptime(date, format))
    except ValueError:
        res = False
    return res





# if __name__ == '__main__':
    
#     now = datetime.now()
#     access_time = now.strftime("%d/%m/%Y %H:%M:%S")

#     #  ["2015-10-01T08:45:10","2015-11-01T19:37:12"]
#     period_of_interest = ["15-10-01T08:45:10","22-11-01T19:37:12"]
    
#     print(request("salad","salads", period_of_interest, 0, access_time))



