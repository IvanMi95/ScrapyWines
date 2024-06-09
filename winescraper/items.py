# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WineItem(scrapy.Item):
    name = scrapy.Field()
    website = scrapy.Field()
    url = scrapy.Field()
    sale_price = scrapy.Field()
    original_price = scrapy.Field()
    lowest_price = scrapy.Field()
    awards = scrapy.Field()
    discount_percentage = scrapy.Field()
    availability = scrapy.Field()
    appellation = scrapy.Field()
    grape_variety = scrapy.Field()
    alcohol_content = scrapy.Field()
    serving_temperature = scrapy.Field()
    wine_type = scrapy.Field()
    vivino_rating = scrapy.Field()
    vivino_reviews = scrapy.Field()
    vivino_url = scrapy.Field()
