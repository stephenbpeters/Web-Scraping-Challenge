from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
# visit our first site
# Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    m_data = {}

# Visit redplanetscience.com/
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

# Scrape first page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    title = soup.find('div', class_='content_title').text
    teaser = soup.find('div', class_='article_teaser_body').text

    m_data["title"] = title
    m_data["teaser"] = teaser

# Scrape second page into Soup   
    url = "https://spaceimages-mars.com/"
    browser.visit(url) 

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    relative_image = soup.find('img', class_='headerimage fade-in')["src"]
    featured_image_url = url + relative_image

    m_data['featured_image'] = featured_image_url

# Scrape third page into Soup  
    url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url)
    mars_info = tables[0]
    mars_info.rename(columns = {0: 'Stats', 1: 'Red Planet', 2: 'Our Planet'}, inplace=True)
    web = mars_info.to_html(index=False, classes='table-striped')

    m_data['planets'] = web

# Scrape fourth page into Soup  
    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')
    hemis = soup.find_all('div', class_="item")
    hemisphere_image_urls = []

    for hemi in hemis:
        h3 = hemi.find('h3')
        name = hemi.find('h3').text
        name_short = name.replace(' Enhanced', '')
        link = hemi.find('a')
        href = link['href']
        newUrl = 'http://marshemispheres.com/' + href
        # go to the sub page
        browser.visit(newUrl)
        time.sleep(1)
        html_sub = browser.html
        soup_sub = bs(html_sub, 'html.parser')
        big_image = soup_sub.find('img', class_='wide-image')
        img_url = url + big_image['src']
        dict = { 'title': name_short, 'img_url': img_url }
        hemisphere_image_urls.append(dict)

    m_data['hemis'] = hemisphere_image_urls    

    # Quit the browser
    browser.quit()

    return m_data