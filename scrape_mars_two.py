from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import time
import pandas as pd

def init_browser():
        browser = Browser('chrome', headless=False)

def scrape():
    #create an empty dictionary to store values
    news_data={}
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(response.text, 'lxml')
    #find the appropriate div class containing target data to scrape, scrape text and assign to variables
    news_p = soup.find_all('div',class_="rollover_description_inner")[0].text.strip()
    news_title = soup.find_all('div',class_="content_title")[0].text.strip()
    #put the variables into a dictionary
    post = {"news_title": news_title,
                    "news_p":news_p}
    print(post)
    #update the main dictionary with the new dictionary 
    news_data.update(post)
    browser = Browser('chrome', headless=False)
    #new URL to scrape 
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    #use splinter to click on button 
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
    #store the full image link in a dictionary
    post_two = {'featured_image':featured_image_url}
    #update the main dictionary with the new dictionary data
    news_data.update(post_two)
    print(post_two)
    #visit the mars twitter page to get the Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    response = requests.get(url)
    #parse HTML with Beautiful soup, get the text
    soup = BeautifulSoup(response.text, 'html.parser')
    #get the text from the first p tag with appropriate class (from inspecting the site)
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #store the weather tweet in a dictionary
    post_three = {'mars_weather':mars_weather}
    #update the maind dictionary with the new dictionary data
    news_data.update(post_three)
    print(post_three)
    browser = Browser('chrome', headless=False)
    #new URL to be scraped
    url = 'https://space-facts.com/mars/'
    #read the table, put into list variable
    tables = pd.read_html(url)
    #convert the list to a dataframe
    mars_df =tables[0]
    #set column names 
    mars_df.columns = ["Characteristics","Values"]
    #set index to Characteristics
    mars_df = mars_df.set_index(["Characteristics"])
    #make it an html table
    mars_df.to_html("mars_data.html")
    #put the whole table into a dictionary item
    table_post={"mars_table":mars_df.to_html()}
    #update the main dictionary with the table dictionary
    news_data.update(table_post) 
    print(table_post)
    browser = Browser('chrome', headless=False)
    #new URL to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all(class_='item')
    #an empty array to store dictionary
    image_data=[]
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
        
        for info in infos:
            link_two=info.find('a')
            img_url=link_two['href']
            post_four={'img_url':img_url, 'title':title}
            image_data.append(post_four)

     #update main dictionary with new data
    post_five={"image_data":image_data}
    print(post_five)
   
    news_data.update(post_five)
    return news_data
            
