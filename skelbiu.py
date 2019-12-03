# -*- coding: utf-8 -*-
"""
@author: Ernestas
"""

from bs4 import BeautifulSoup
import requests
import csv 
import time 
import re

def write_row(rows, filename):
    with open(filename, 'a', encoding='utf_8_sig') as toWrite:
        writer = csv.writer(toWrite, lineterminator='\n')
        writer.writerow(rows)
    toWrite.close()
    
def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

    # fetching the url, raising error if operation fails
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        exit()

    return BeautifulSoup(response.text, "html.parser")
    
def get_ads_urls(url, base):
    soup = get_soup(url)
    links = []
    
    for link in soup.find_all('a', 'adsImage js-cfuser-link'):
        links.append(base+link.get('href'))

    return links

def get_id_from_url(url):
    return url.rsplit('-', 1)[1].replace('.html', "")

def get_data(url):
    
    
    soup = get_soup(url)
    
    # logic to parse and return data about apartment
    try:
        price = re.sub('[^0-9\,]', '', soup.find("p", "price").text)
        city = ''
        years = ''
        area = ''
        rooms = ''
        
        for details in soup.find_all('div', 'detail'):
            title = details.find('div', 'title').text.strip()
            if(title == 'Gyvenvietė:'):
                city = details.find('div', 'value').get_text(strip=True, separator=',').strip().split(',')[0]
            if(title == 'Kamb. sk.:'):
                rooms = re.sub('[^0-9]', '', details.find('div', 'value').text)
            if(title == 'Metai:'):
                years = re.sub( r"([^0-9])", r" \1", details.find('div', 'value').text).split()[0]
            if(title == 'Plotas, m²:'):
                area = re.sub('[^0-9\,]', '', details.find('div', 'value').text)
        
        return [city, years, area, rooms, price, url]
    except:
        return False

if __name__ == "__main__":
    filename = "soup_skelbiu_"+time.strftime("%Y_%m_%d-%H%M")+".csv"
    
    # prep file header
    write_row(['city', 'years', 'area', 'rooms', 'price', 'url'], filename)
    
    # urls
    base = 'https://www.skelbiu.lt'
    base_url = "https://www.skelbiu.lt/skelbimai/"
    page = 1
    search = "?autocompleted=1&keywords=&cost_min=&cost_max=&space_min=&space_max=&rooms_min=&rooms_max=&year_min=&year_max=&building=0&status=1&floor_min=&floor_max=&floor_type=0&import=2&searchAddress=&district=0&quarter=0&streets=0&ignorestreets=0&cities=0&distance=0&mainCity=0&search=1&category_id=41&type=1&user_type=0&ad_since_min=0&ad_since_max=0&visited_page=1&orderBy=-1&detailsSearch=1"
    
    
    # collect only urls
    # scrap them (city, years, area, rooms, price, '', url)
    
    while(page <= 43):
    # get urls and cities from list page    
        print("Page: "+str(page))
        urls = get_ads_urls(base_url+str(page)+search, base)
        page += 1
        time.sleep(.3)
        for url in urls:
            data = get_data(url)
            if(data):
                print("Writing id: "+ get_id_from_url(url))
                write_row(data, filename)
                time.sleep(.555)
            else:
                print("Skipping id: "+ get_id_from_url(url))
    print("Complete")
     
