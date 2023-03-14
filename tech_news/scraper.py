import requests
from time import sleep
from parsel import Selector


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    sleep(1)
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code != 200:
            return None

        return response.text
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)

    news_urls = selector.css('.entry-title a::attr(href)').getall()

    if not news_urls:
        return []

    return news_urls


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
