from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
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

    # Quit the browser
    browser.quit()

    return m_data