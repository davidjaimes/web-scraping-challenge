# Import all dependencies.
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


def scrape():
    # Path to driver for macOS.
    # Needed to serve content properly.
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #  Visit NASA Mars News website with Chrome driver
    # and parse html with Beautiful Soup.
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')

    # Scrape and collect the latest news title and paragraph text.
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Create Complete Dictionary
    mars_data = {
        'news_title': news_title,
        'news_p': news_p
    }

    return mars_data
