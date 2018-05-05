
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import time
import pandas as pd

def init_browser():
        browser = Browser('chrome', headless=False)

def scrape():
   
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(response.text, 'lxml')
    #grabbling the 'slide' class element from the url
    results = soup.find_all(class_="slide")
    #creating a list to hold scraped data
    news_data=[]
    for result in results:
    # Error handling
        try: #loop thru and get the text within these classes, replace \n with blank space
            news_p = result.find(class_="rollover_description_inner").text.replace('\n', '')
            news_title = result.find(class_="content_title").text.replace('\n', '')
           
            post = {"news_title": news_title,
                    "news_p":news_p}

            news_data.append(post)
            
          
        except Exception as e:
               print(e)
    browser = Browser('chrome', headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    #use splinter to click the "Full Image" button
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    #HTML Object 
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    #find the class where pic is stored
    results = soup.find(class_='fancybox-image')
    #retrieve source attribute, i.e. the path
    url = results['src']
    #attach the path to the main site link, this is the full image link
    featured_image_url = 'https://www.jpl.nasa.gov'+url
    post_two = {'featured_image':featured_image_url}
    news_data.append(post_two)
    #visit the mars twitter page to get the Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    response = requests.get(url)
    #parse HTML with Beautiful soup, get the text
    soup = BeautifulSoup(response.text, 'html.parser')
    #get the text from the first p tag with appropriate class (from inspecting the site)
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    post_three = {'mars_weather':mars_weather}
    news_data.append(post_three)
    browser = Browser('chrome', headless=False)
    #visit the mars space facts site
    url = 'https://space-facts.com/mars/'
    #read the table, put into list variable
    tables = pd.read_html(url)
    #convert the list to a dataframe
    mars_df =tables[0]
    #put column headers on 
    mars_df.columns = ["Characteristic", "Value"]
    #convert the datframe to dictionary, using 'records' orientation, this does not neeed to be, nor should be, appended to news_data, as will create a list of a dictionary within the list, and not be able to be inserted to mongodb
    mars_dict=mars_df.to_dict('records')
    #Visit the site to get images of Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all(class_='item')
    #an empty array to store dictionary
    mars_images=[]
    #loop through the item class
    for result in results:
        #find the first a tag
        link=result.find('a')
        #assign the href to variable 'links'
        links = link['href']
        #assign the link h3 title text to variable 'title'
        title =result.find('h3').text
        #concatenate the path with the main site link, assign to variable 'url'
        url='https://astrogeology.usgs.gov'+links
        #open brower, chromedriver
        browser = Browser('chrome', headless=False)
        #visit the concatenated url
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        #parse the html with beautiful soup
        soup = BeautifulSoup(html, 'html.parser')
        #find all elemenst with class 'downloads', assign results to variable list 'infos'
        infos = soup.find_all(class_='downloads')
        #loop thru infos, pull out links to images, assign with title to dictionary post, and then append to list
        #mars_images
        for info in infos:
            link_two=info.find('a')
            img_url=link_two['href']
            post_four={'img_url':img_url, 'title':title}
            news_data.append(post_four)
  
   
   #return your data, so it can be accessed by flask app (where the insertion into mongodb will occur)
    return news_data+mars_dict
    
            