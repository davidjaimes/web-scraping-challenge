# Import all dependencies.
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


def scrape():
    try:
        # Path to driver for macOS.
        # Needed to serve content properly.
        executable_path = {'executable_path': 'chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)

        #  Visit NASA Mars News website with Chrome driver
        # and parse html with Beautiful Soup.
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        browser.is_element_present_by_css('.article_teaser_body', wait_time=1)
        soup = BeautifulSoup(browser.html, 'html.parser')

        # Scrape and collect the latest news title and paragraph text.
        news_title = soup.find('div', class_='content_title').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Visit JPL Mars Space Images website with chrome driver
        # and parse html with Beautiful Soup.
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        soup = BeautifulSoup(browser.html, 'html.parser')

        # Scrape and collect the full size, image url for current Featured Mars Image.
        base_url = 'https://www.jpl.nasa.gov'
        image_url = soup.find('li', class_='slide').a['data-fancybox-href']
        featured_image_url = base_url + image_url

        # Visit Mars Weather twitter account with chrome driver
        # and parse html with Beautiful Soup.
        url = 'https://twitter.com/marswxreport?lang=en'
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')

        # Scrape and collect latest Mars weather tweet.
        for find in soup.find_all('div', class_='js-tweet-text-container'):
            if find.p.text[:11] == 'InSight sol':
                mars_weather = find.p.text
                break

        # Visit the Mars Facts website with chrome driver.
        url = 'https://space-facts.com/mars/'
        browser.visit(url)
        df = pd.read_html(browser.html)
        df[0].columns = ['Description', 'Value']
        df[0].set_index('Description', inplace=True)
        html_table = df[0].to_html()

        # Visit the Mars Hemispheres website with chrome driver
        # and parse html with Beautiful Soup.
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        soup = BeautifulSoup(browser.html, 'html.parser')

        # Scrape and collect high resolution images for each
        # of Mars' hemispheres.
        base_url = 'https://astrogeology.usgs.gov'
        hemisphere_image_urls = []
        for item in soup.find_all('div', class_='item'):
            title = item.h3.text
            image_url = item.find('a', class_='itemLink product-item')['href']

            # Visit individual hemisphere website to scrape and collect full size image.
            browser.visit(base_url + image_url)
            soup = BeautifulSoup(browser.html, 'html.parser')
            image_url = soup.find('img', class_='wide-image')['src']

            # Append dictionary to list
            hemisphere_image_urls.append({'title': title, 'image_url': base_url + image_url})

        # Create Complete Dictionary
        mars_data = {
            'news_title': news_title,
            'news_p': news_p,
            'featured_image_url': featured_image_url,
            'mars_weather': mars_weather,
            'html_table': html_table,
            'hemisphere_image_urls': hemisphere_image_urls
        }

        return mars_data

    finally:
        browser.quit()
