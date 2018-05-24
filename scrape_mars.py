import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import requests

def init_browser():
    executable_path = {'executable_path': 'C:/Users/marks/OneDrive/Desktop/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
def scrape():
    executable_path = {'executable_path': 'C:/Users/marks/OneDrive/Desktop/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    mars = {}
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = soup.find_all('div', class_="slide")
    
    for result in results:
        mars['headline']=result.find('div', class_="content_title").text
        mars['text']=result.find('div', class_="rollover_description").text
    
    
    url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)
    mars['featuredimg1']=soup.find('img')['src']
    mars['featuredimg']=url+mars['featuredimg1']

    
    twitter = 'https://twitter.com/marswxreport?lang=en'
    
    response = requests.get(twitter)
    
    soup = BeautifulSoup(response.text, 'html.parser')
        
    results = soup.find_all('div', class_="dir-ltr")
    

    mars['weather']=results[2].text

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df=tables[0]
    mars['table']=df
    
    
    
    url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_='itemLink product-item')
    
    title_list=[]
    url_list=[]
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    for result in results:
        try:
            title=result.find('h3').text
            title_list.append(title)
    
        except AttributeError as e:
            print(e)
                
    url_list.append('https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg')
    url_list.append('https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg')
    url_list.append('https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg')
    url_list.append('https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg')
    
    keys=['title', 'img_url']
    import itertools
    dictionary=dict(zip(title_list, url_list))
    
    return mars