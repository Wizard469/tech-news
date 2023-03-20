from tech_news.database import find_news
from collections import Counter


# Requisito 10
def top_5_categories():
    categories = sorted([news["category"] for news in find_news()])

    return [key[0] for key in Counter(categories).most_common(5)]
