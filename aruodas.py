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
 
def get_ads_urls(url):
   
    soup = get_soup(url)

    cities_links = [];
    
    for title in soup.find_all('h3'):
        data = {
           'city': '',
           'url': '',        
        }
        try:
            data['url'] = title.find('a').get('href')
            data['city'] = title.get_text(strip=True, separator=',').strip().split(',')[0]
            cities_links.append(data);
        except:
            print('Failed to get url '+title.text)
        

            
    return cities_links

def get_data(city_url):
    
    
    url = city_url['url']
    soup = get_soup(url)
    
    # logic to parse and return data about apartment
    try:
        price = re.sub('[^0-9\,]', '', soup.find("span", "price-eur").text)
        city = city_url['city']
        years = ''
        area = ''
        heat = ''
        rooms = ''
        created_at = ''
        updated_at = ''

        simple_stats = soup.find("div", class_="obj-stats simple")
        simple_stats_features = []

        for stat in simple_stats.find_all("dt"):
            feature_key = stat.text.strip()
            simple_stats_features.append([feature_key])

        for key, stat in enumerate(simple_stats.find_all("dd")):
            feature_key = stat.text.strip()
            simple_stats_features[key].append(feature_key)

        for feature in simple_stats_features:
            if(feature[0] == "Įdėtas"):
                created_at =  feature[1]
            if(feature[0] == 'Redaguotas'):
                updated_at = feature[1]
        
        dl_data = soup.find("dl", class_="obj-details")

        features = []
        for  dt_item in dl_data.find_all("dt"):
            feature_key = dt_item.text.strip()
            
            features.append([feature_key])
            
        for key, dt_item in enumerate(dl_data.find_all("dd")):
            feature_key = dt_item.text.strip()
            features[key].append(feature_key)
                
        for feature in features:
            if(feature[0] == "Metai:"):
                years = re.sub( r"([^0-9])", r" \1", feature[1]).split()[0]
            if(feature[0] == "Plotas:"):
                area =  re.sub('[^0-9\,]', '', feature[1])
            if(feature[0] == 'Kambarių sk.:'):
                rooms = re.sub('[^0-9\,]', '', feature[1])
                
        
        soup = get_soup(get_ajax_url(get_id_from_url(url)))
        
        for item in soup.find_all("div", "statistic-info-row"):
            if(item.find("div", "icon-heating-gray")):
                heat = re.sub('[^0-9\,]', '', item.find('span', 'cell-data cell-data-inline-block').contents[0])
        
        
        return [city, years, area, rooms, price, heat, created_at, updated_at, url]
    except:
        return False
    
def get_id_from_url(url):
    return url.rsplit('-', 1)[1].replace('/', "")

def get_ajax_url(item_id):
    return "https://www.aruodas.lt/ajax/getAdvertStatistics/?objTypeId=1&advertId="+item_id

if __name__ == "__main__":
    filename = "soup_aruodas_"+time.strftime("%Y_%m_%d-%H%M")+".csv"
 
    # prep file header
    write_row(['city', 'years', 'area', 'rooms', 'price', 'avg_heat_per_m', 'created_at', 'updated_at', 'url'], filename)
    
    # get urls from page
    url = "https://www.aruodas.lt/butai/puslapis/"
    page = 1
    search = "/?FHouseState=full"
    

    while(page <= 248):
    # get urls and cities from list page    
        print("Page: "+str(page))
        cities_urls = get_ads_urls(url+str(page)+search)
        page += 1
        time.sleep(1)
        for item in cities_urls:
            data = get_data(item)
            if(data):
                print("Writing id: "+ get_id_from_url(item['url']))
                write_row(data, filename)
                time.sleep(1)
            else:
                print("Skipping id: "+ get_id_from_url(item['url']))
    print("Complete")
     