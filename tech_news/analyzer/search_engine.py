from tech_news.database import search_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    return [
        (news["title"], news["url"])
        for news in search_news({"title": {"$regex": title, "$options": "i"}})
    ]


# Requisito 8
def search_by_date(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")

    return [
        (news["title"], news["url"])
        for news in search_news({"timestamp": {"$regex": date}})
    ]


# Requisito 9
def search_by_category(category):
    return [
        (news["title"], news["url"])
        for news in search_news({"category": {
            "$regex": category, "$options": "i"
        }})
    ]
