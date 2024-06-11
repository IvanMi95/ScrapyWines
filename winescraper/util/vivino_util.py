from typing import Any, Optional
import requests
from winescraper.util.pipe_util import clean_string
from scrapy.selector import Selector


def construct_vivino_query(wine_name: str) -> str:
    if not isinstance(wine_name, str):
        raise ValueError("Name is not a string")
    wine_name = clean_string(value=wine_name)
    wine_name_list = wine_name.split(" ")
    wine_query = '+'.join([wine for wine in wine_name_list])
    url = f"https://www.vivino.com/search/wines?q={wine_query}"
    return url


def make_vivino_request(wine_name: Any) -> Any:
    if not isinstance(wine_name, str):
        raise ValueError("Name is not a string")
    wine_name = clean_string(value=wine_name)
    base_url = "https://www.vivino.com"
    search_url = "https://www.vivino.com/search/wines"
    params = {
        'q': wine_name
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-Gpc': '1',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': 'insert your cookie data here'
    }

    response = requests.get(search_url, headers=headers, params=params)
    sel = Selector(text=response.text)
    rating = sel.xpath("//div[contains(@class, 'average__number')]/text()").get()
    reviews = sel.xpath(
        "//div[contains(@class, 'average__stars')]//p[@class='text-micro']/text()").get()
    vivino_url = sel.xpath(
        "//div[@class='search-results-list']/div[@class='card card-lg']//a/@href").get()
    vivino_rating = clean_vivino_rating(raw_rating_string=rating)
    vivino_reviews = clean_vivino_number_reviews(raw_review_string=reviews)
    return {
        'vivino_rating': vivino_rating,
        'vivino_reviews': vivino_reviews if vivino_rating is not None else None,
        "vivino_url": base_url + vivino_url.strip() if vivino_url else None
    }


def clean_vivino_rating(raw_rating_string: str | None) -> Optional[float]:
    if not isinstance(raw_rating_string, str):
        if isinstance(raw_rating_string, float):
            return raw_rating_string
        return None
    rating_string = raw_rating_string.replace(",", ".").strip()
    try:
        return float(rating_string)
    except ValueError:
        return None


def clean_vivino_number_reviews(raw_review_string: str | None) -> Optional[int]:
    if not isinstance(raw_review_string, str):
        if isinstance(raw_review_string, int):
            return raw_review_string
        return None

    review_string = raw_review_string.strip()
    review_string_list = review_string.split(" ")

    try:
        return int(review_string_list[0])
    except ValueError:
        return None
