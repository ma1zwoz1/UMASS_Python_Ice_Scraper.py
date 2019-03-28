#!/usr/bin/python
#Week 6 INFO 3050.060 Python Assignment
#Zachary Wozich
#The program is a semi complex web scraper type of Python program and is a duplicate of the Week3 Perl web scraper.
#It downloads all text based weather
#alerts for the east coast and only gives the "hazardous weather outlook" for
#the weather station in Gray Maine since I live in Southern Maine and I only
#care about winter weather alerts.
#This program then prints the output to a text file.
#The program is called by typing python Ice_Scraper.py

import sys #for printing to file
import os #to get current working directory
from requests import get #gets the URL
from requests.exceptions import RequestException #print exceptions to HTTP failures
from contextlib import closing # Closes HTTP connection
from bs4 import BeautifulSoup # Python WedScraper Library

def simple_get(url):
    """
    This function attempts to get the content at `url` by making an HTTP GET request using the requests librarys.
    If the content-type of response is some kind of HTML/XML, return the
    text content or none.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    This function returns True if the response seems to be HTML, False otherwise using the requests librarys.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
   This function prints any errors 
    """
    print(e)

def get_events():
    """
    This function downloads and scrapes the page where the list of alerts is found
    and returns a list using the Beautiful Soup Library. Also prints Title
    """
    heads = set()
    url = 'https://www.weather.gov/wwamap/wwatxtget.php?cwa=gyx&wwa=all'
    response = simple_get(url)
    html = BeautifulSoup(response, 'html.parser')
    for title in html.select('title'):
            for head in title:
                if len(head) > 0:
                    #strip text
                    heads.add(head.strip())
    print(heads)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        events = set()
        #grab the target HTML pag 'pre'
        for pre in html.select('pre'):
            for event in pre:
                if len(event) > 0:
                    #strip text
                    events.add(event.strip())
        return list(events)
    
    
    
    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(url))   

def event_filter():   
   """
    This function filters the dowloaded scrapped output then print to file
   """ 
   dirpath = os.getcwd()+"/Ice_Scraper_Output.txt"

   for x in events:
    x= x.replace("\n", ' ')
    #(filter by the two strings below)
    if 'National Weather Service Gray ME' in x and 'Hazardous Weather Outlook' in x:
        print('1',x)
        #print to screen
        original = sys.stdout
        sys.stdout = open(dirpath, 'a+')
        print('{National Weather Service Watch Warning Advisory Summary}')
        #print stdout to file
        print('1',x)
        sys.stdout = original
    elif 'National Weather Service Gray ME' in x:
        print('1',x)
        original = sys.stdout
        sys.stdout = open(dirpath, 'a+')
        print('1',x)
        sys.stdout = original               
        print('No Hazardous Events in Gray ME Today Professor Marks but here are others!')

        
if __name__ == '__main__':
    print('Getting the list of filtered events....')
    events = get_events()
    print() #print space
    events_filtered = event_filter()
    print() #print space
    print('... filtered events printed.\n')
    dirpath = os.getcwd()+"/Ice_Scraper_Output.txt"
    print("current File Path is : " + dirpath)
    print() #print space
    foldername = os.path.basename(dirpath)
    print("File Name is : " + foldername)




       
 
