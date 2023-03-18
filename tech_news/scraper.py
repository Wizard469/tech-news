import requests
from time import sleep
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    sleep(1)
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code != 200:
            return None

        return response.text
    except (requests.ReadTimeout, requests.exceptions.TooManyRedirects):
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)

    return selector.css(".entry-title a::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)

    return selector.css(".next.page-numbers::attr(href)").get()


# Requisito 4
def scrape_news(html_content):
    if not isinstance(html_content, str):
        return None

    selector = Selector(text=html_content)

    url = selector.css("link[rel='canonical']::attr(href)").get()
    title = selector.css("h1.entry-title::text").get().rstrip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css(".author a::text").get()
    reading_time = int(
        selector.css(".meta-reading-time::text").re_first(r"\d+") or 0
    )
    first_paragraph = selector.css(
        ".entry-content > p:first-of-type *::text"
    ).getall()
    category = selector.css(".label::text").get()

    summary = "".join(first_paragraph).rstrip()

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):
    updates_url = "https://blog.betrybe.com/"
    all_news = []

    while len(all_news) < amount:
        html_content = fetch(updates_url)
        new_urls = scrape_updates(html_content)
        updates_url = scrape_next_page_link(html_content)

        for url in new_urls:
            if len(all_news) < amount:
                html_content = fetch(url)
                all_news.append(scrape_news(html_content))

    create_news(all_news)

    return all_news
