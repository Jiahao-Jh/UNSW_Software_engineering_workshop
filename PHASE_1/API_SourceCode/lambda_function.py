from datetime import datetime, date
import re
from geotext import GeoText

from Article import Article
from Report import Report
from location import Location
from json import dumps

'''
File: Article.py
File Created: Friday, 11th March 2022 6:04:38 pm
Author: Hu Shuhao (hu.shuhao@outlook.com)
'''

from bs4 import BeautifulSoup
import requests

month_dict = {
    'Feb ': 'February ',
    'Jan ': 'January ',
    'Apr ': 'April ',
    'Sep ': 'September ',
}


def iter_terms(key_terms, city, start_date, end_date):
    res_list = list()
    for term in key_terms:
        first_letter = term[0].lower()
        if not first_letter.isalpha():
            first_letter = '0'
        index_url = f'https://www.cdc.gov/az/{first_letter}.html'
        source = requests.get(index_url).text
        soup = BeautifulSoup(source, 'html.parser')

        link_tags = soup.find_all(lambda tag: tag.name == 'a' and term.strip().
            lower() in tag.text.strip().lower())
        link_set = set()
        for link in link_tags:
            link_set.add(link.get('href'))

        for link in link_set:
            source = requests.get(link).text
            soup = BeautifulSoup(source, 'html.parser')
            article = Article(url=link)
            res_list.append(article)
            main_text = ''
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                if len(p.text) >= 100:
                    main_text = p.text
                    break
            if main_text == '':
                main_text = soup.p.text

            article['main_text'] = main_text
            headline = soup.find('title')
            if headline is not None:
                article['headline'] = headline.text
            if term.strip().lower() == 'salmonella':
                parse_salmonella(article, soup, city, start_date, end_date)
            elif term.strip().lower() == 'measles':
                parse_measles(article, soup, city, start_date, end_date)
            elif term.strip().lower() == 'ebola':
                parse_ebola(article, soup, city, start_date, end_date)
            elif term.strip().lower() == 'hantavirus':
                parse_hantavirus(article, soup, city, start_date, end_date)
            else:
                article['reports'] = f'Current scraper does not support searching {term}'
    return res_list


def parse_salmonella(article, soup, query_city, start_date, end_date):
    outbreaks_link = soup.find(
        lambda tag: tag.name == 'a' and tag.text == 'More')
    if outbreaks_link is not None:
        source = requests.get('https://www.cdc.gov/' +
                              outbreaks_link.get('href')).text
        soup = BeautifulSoup(source, 'html.parser')
        for year in range(start_date.year, end_date.year + 1):
            year_section = soup.find(lambda tag: tag.name == 'a' and re.compile(r'\d{4} Outbreaks').match(tag.text))
            if year_section is None:
                continue
            report_links = year_section.parent.find_all(lambda tag: tag.name == 'a' and 'index.html' in tag.get('href'))
            for report_link in report_links:
                source = requests.get('https://www.cdc.gov' + report_link.get('href')).text
                soup = BeautifulSoup(source, 'html.parser')
                text = soup.get_text()

                e = re.search(
                    r'(January|February|March|April|May|June|July|August|September|October|November|December) \d{2}, '
                    r'\d{4}, to (January|February|March|Apirl|May|June|July|August|September|October|November'
                    r'|December) \d{2}, \d{4}', text)
                event_date = e.group()

                if event_date is None:
                    continue
                report_start_str = event_date.split(', to')[0]
                report_start = datetime.strptime(report_start_str, '%B %d, %Y')
                if not start_date <= report_start <= end_date:
                    continue
                case_tag = soup.find(
                    lambda tag: (tag.name == 'li' or tag.name == 'a') and
                                (tag.text == 'Reported Cases:' or tag.text == 'Case Count'))
                if case_tag.name == 'a':
                    case_number = int(
                        re.sub(',', '', case_tag.parent.text.split(': ')[1]))
                else:
                    case_number = int(case_tag.text)
                hospitalization_tag = soup.find(lambda tag: tag.name == 'li' and tag.text == 'Hospitalizations:')
                if hospitalization_tag is not None:
                    hospitalization_number = int(hospitalization_tag.text)
                else:
                    hospitalization_number = 0
                disease = soup.find(lambda tag: tag.name == 'em').text
                death = soup.find(
                    lambda tag: tag.name == 'li' and tag.text == 'Deaths:')
                if death is not None:
                    death = int(death.text)
                else:
                    death = 0
                cities = GeoText(text).cities
                cities = set(cities)
                if query_city != 'all' and query_city not in cities:
                    continue
                locations = list()
                for city in cities:
                    if city == 'Most' or city == 'Of' or city == 'March':
                        continue
                    locations.append(Location(city=city))

                report = Report(disease, cases=case_number, hospitalization=hospitalization_number, death=death,
                    locations=locations, event_date=event_date)
                article['reports'].append(report)


def parse_measles(article, soup, query_city, start_date, end_date):
    outbreaks_link = soup.find(
        lambda tag: tag.name == 'a' and tag.text == 'Cases and Outbreaks')
    if outbreaks_link is not None:
        link = 'https://www.cdc.gov/' + outbreaks_link.get('href')
        source = requests.get(link).text
        soup = BeautifulSoup(source, 'html.parser')
        for li in soup.find_all(lambda tag: tag.name == 'li' and re.compile(
                r'.*(January|February|March|April|May|June|July|August|September|October|November|December).*'
        ).match(tag.text)):
            report_start_str = li.text.split('MMWR')[-1]
            report_start_str = re.sub(r'[,\.]', '', report_start_str.strip())
            report_start_str = report_start_str.strip()
            if 'Vol' in report_start_str or 'From' in report_start_str:
                continue
            for abbr, full in month_dict.items():
                report_start_str = re.sub(abbr, full, report_start_str)
            report_start = datetime.strptime(report_start_str, '%B %d %Y')
            if not start_date <= report_start <= end_date:
                continue
            url = li.find('a').get('href')
            if 'https' not in url:
                continue
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'html.parser')
            cities = GeoText(soup.get_text()).cities
            cities = set(cities)
            locations = list()
            if query_city != 'all' and query_city not in cities:
                continue
            for city in cities:
                if city == 'Of' or city == 'Most' or city == 'March':
                    continue
                locations.append(Location(city=city))
            report = Report('measles', locations=locations, event_date=report_start_str)
            article['reports'].append(report)


def find_cases_deaths(text):
    cases = 'Not specified'
    for s in text.split(' cases'):
        num_str = s.split(' ')[-1]
        if num_str.isdigit():
            cases = num_str
            break
    deaths = 'Not specified'
    for s in text.split(' deaths'):
        num_str = s.split(' ')[-1]
        if num_str.isdigit():
            deaths = num_str
            break
    return cases, deaths


def parse_ebola(article, soup, query_city, start_date, end_date):
    outbreaks_link = soup.find(
        lambda tag: tag.name == 'a' and tag.text == 'Outbreaks')
    if outbreaks_link is None:
        return
    source = requests.get(
        'https://www.cdc.gov/vhf/ebola/outbreaks/index-2018.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fvhf'
        '%2Febola%2Foutbreaks%2Findex.html '
    ).text
    soup = BeautifulSoup(source, 'html.parser')
    report_links = [
        link.get('href') for link in soup.find_all(
            lambda tag: tag.name == 'a' and '/vhf/ebola/outbreaks/' in tag.get(
                'href') and any(map(str.isdigit, tag.get('href'))))
    ]
    for link in report_links:
        source = requests.get('https://www.cdc.gov' + link).text
        soup = BeautifulSoup(source, 'html.parser')
        pattern = re.compile(r'^[/[a-z]\.]*$')
        if '2016' not in link and '2014' in link:
            for span in soup.find_all('span'):
                try:
                    event_date = datetime.strptime(span.text, '%B %d, %Y')
                    if not start_date <= event_date <= end_date:
                        continue
                    report_text = span.parent.parent.parent.get_text()
                    cases, deaths = find_cases_deaths(report_text)
                    cities = GeoText(report_text).cities
                    cities = set(cities)
                    if query_city != 'all' and query_city not in cities:
                        continue
                    locations = list()
                    for city in cities:
                        if city == 'Of' or city == 'Most' or city == 'March':
                            continue
                        location = Location(city=city)
                        locations.append(location)
                    report = Report('ebola', event_date=span.text, cases=cases, death=deaths, locations=locations)
                    article['reports'].append(report)
                except:
                    continue
        elif '2014' in link and '2016' in link:
            event_date = '2014 - 2016'
            cases = '28600'
            deaths = '11325'
            locations = [
                Location(county='Guinea'),
                Location(county='Liberia'),
                Location(county='Sierra Leone')
            ]
            report = Report('ebola',
                locations=locations,
                event_date=event_date,
                cases=cases,
                death=deaths)
            article['reports'].append(report)
        elif pattern.match(link):
            continue
        else:
            overview = soup.find(lambda tag: tag.text == 'Overview')
            p = overview.parent.p
            if p is None:
                continue
            p_text = re.sub(',', '', p.text)
            p_text = ' '.join(p_text.split(' ')[1:4])
            event_date = datetime.strptime(p_text, '%B %d %Y')
            if not start_date <= event_date <= end_date:
                continue
            report_text = overview.parent.get_text()
            cases, deaths = find_cases_deaths(report_text)
            cities = GeoText(soup.text).cities
            cities = set(cities)
            if query_city != 'all' and query_city not in cities:
                continue
            locations = list()
            for city in cities:
                if city == 'Most' or city == 'Of' or city == 'March':
                    continue
                locations.append(Location(city=city))
            report = Report('ebola',
                event_date=p_text,
                cases=cases,
                death=deaths,
                hospitalization='Not specified', locations=locations)
            article['reports'].append(report)


def parse_hantavirus(article, soup, city, start_date, end_date):
    outbreaks_link = soup.find(lambda tag: tag.name == 'a' and tag.text == 'Outbreaks')
    if outbreaks_link is None:
        return
    source = requests.get('https://www.cdc.gov' + outbreaks_link.get('href')).text
    soup = BeautifulSoup(source, 'html.parser')
    spans = soup.find_all(lambda tag: tag.name == 'span' and re.compile(
        r'(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}')
        .match(tag.text))
    for span in spans:
        event_date = span.text
        if not trunc_datetime(start_date) <= datetime.strptime(event_date.strip(), '%B %Y') <= trunc_datetime(end_date):
            continue
        report = Report('hantavirus', event_date=event_date)
        article['reports'].append(report)


# from stackoverflow
# https://stackoverflow.com/questions/48457027/how-to-compare-two-dates-based-on-month-and-year-only-in-python
def trunc_datetime(someDate):
    return someDate.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

def error(code, message):
    response = {}
    response["statusCode"] = code
    response["headers"]={}
    response["headers"]['Content-Type']= 'application/json'
    response["body"] = message
    return response

def lambda_handler(event, content):
    
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
    
    if location == "" or key_term == "":
        return error(400,  "Check the value of parameters")
    
           
    period_of_interest = event['multiValueQueryStringParameters']['period_of_interest']  
    
    period_of_interest[0] = period_of_interest[0].split("T")[0]
    period_of_interest[1] = period_of_interest[1].split("T")[0]
    try:
        start_date = datetime.strptime(period_of_interest[0], '%y-%m-%d')
        end_date = datetime.strptime(period_of_interest[1], '%y-%m-%d')
    except:
        return error(400,  "Check the value of parameters, Incorrect date format")

    res = iter_terms(key_term ,location , start_date, end_date)
    
    if res == []:
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

if __name__ == '__main__':
    for l in iter_terms(['salmonella'], 'Beni', datetime(2020, 1, 1), datetime(2020, 12, 1)):
        print(l.json())
