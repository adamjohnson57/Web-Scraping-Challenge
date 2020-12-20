from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def scrape_mars():
    executable_path = {'executable_path': "C:/Users/adamj/bin/chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    title = soup.find_all('div', class_='content_title')
    paragraph = soup.find_all('div', class_='article_teaser_body')
    news_title = title[1].text
    news_p = paragraph[0].text
    print(f"news_title= {news_title}")

    base_url = "https://www.jpl.nasa.gov"
    url = base_url + "/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')


    img_url = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    feat_img_url = base_url + img_url



    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    mars_facts = pd.read_html(facts_url)[0]
    mars_facts_html = mars_facts.to_html()
    


    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    base_url = "https://astrogeology.usgs.gov"
    time.sleep(3)
    hemi_html = browser.html
    soup = bs(hemi_html, 'html.parser')

    items = soup.find_all('div', class_='description')
    hemi_img_url = []

    for i in items:
        hemi_name = str(i.find('a').text).replace(" Enhanced", "")
        img_url = i.find('a')['href']
        url = base_url + img_url
        browser.visit(url)
        time.sleep(3)
        hemi_link = browser.html
        hemi_soup = bs(hemi_link, 'html.parser')
        hemi_img = base_url + hemi_soup.find('img', class_="wide-image")['src']
        
        hemi_img_url.append({"Title": hemi_name, "IMG_URL": img_url})

    browser.quit()

    mars_page = {}
    mars_page["news_title"] = news_title
    mars_page["news_p"] = news_p
    mars_page["feat_img_url"] = feat_img_url
    mars_page["mars_facts_html"] = mars_facts_html
    mars_page["hemi_img_url"] = hemi_img_url

    return mars_page

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_mars())


