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
    selector = Selector(text=html_content)

    next_page_url = selector.css('.next.page-numbers::attr(href)').get()

    if not next_page_url:
        return None

    return next_page_url


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)

    url = selector.css("link[rel='canonical']::attr(href)").get()
    title = selector.css('h1.entry-title::text').get().replace("\xa0", "")
    timestamp = selector.css('li.meta-date::text').get()
    writer = selector.css('.author a::text').get()
    reading_time = selector.css('.meta-reading-time::text').re_first(r'\d+')
    first_paragraph = selector.css(
        '.entry-content > p:first-of-type *::text'
    ).getall()
    category = selector.css('.label::text').get()

    summary = "".join(first_paragraph).replace("\xa0", "")

    suffix = " "
    if title.endswith(suffix):
        # title = title[:-len(suffix)]
        title = title.removesuffix(suffix)
    if summary.endswith(suffix):
        summary = summary.removesuffix(suffix)

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": int(reading_time),
        "summary": summary,
        "category": category
    }


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
