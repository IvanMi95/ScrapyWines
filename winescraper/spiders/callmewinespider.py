from typing import List
from scrapy import Request, Spider
from scrapy.http import Response
from scrapy.selector.unified import Selector, SelectorList
from scrapy_playwright.page import PageMethod

from winescraper.config.settings_config import get_callmewine_settings_without_vivino, get_tannico_settings, get_tannico_settings_without_vivino
from winescraper.items import WineItem
from winescraper.util.vivino_util import construct_vivino_query, make_vivino_request
# scrapy crawl tannicospider


class CallMeWineSpider(Spider):
    name = "callmewinespider"
    allowed_domains = ["www.callmewine.com"]
    start_urls = ["https://www.callmewine.com/pages/vini-in-offerta"]
    custom_settings = get_callmewine_settings_without_vivino()
# response.xpath('//div[@class="c-productBox__image relative"]/a/@href').get()

    def parse(self, response):
        product_links = response.xpath(
            '//div[@class="products-grid"]//a[@aria-label="Vai alla pagina dei dettagli del prodotto"]/@href').getall()

        for url in product_links:
            yield response.follow(
                url=url,
                callback=self.parse_wine,
                meta={
                    "wine_page_url": url,
                    "website": "www.callmewine.com"
                }
            )

    def parse_wine(self, response: Response):

        wine_item = WineItem()
        wine_item["original_price"] = response.xpath(
            '//div[@data-v-742ea495]//div[@data-v-742ea495]//span[contains(@class, "line-through") and contains(@class, "text-gray-dark") and contains(@class, "text-sm")]/text()').get()
        wine_item["name"] = response.xpath(
            '//h1[@class="h2 text-secondary <md:pt-8"]/text()').get()
        wine_item["url"] = response.meta['website'] + response.meta['wine_page_url']
        wine_item["website"] = response.meta['website']
        wine_item["sale_price"] = response.xpath(
            'concat(//span[@class="c-finalPrice__integer inline-block leading-none cmw-font-bold m-0 -regular"]/text(), ",", //span[@class="c-finalPrice__fraction -regular"]/text(), "€")').get()

        wine_item["original_price"] = response.xpath(
            '//span[contains(@class, "line-through") and contains(@class, "text-gray-dark") and contains(@class, "text-sm")]/text()').get()
        wine_item["lowest_price"] = response.css(
            'span.text-xxs.sm\\:text-xs.text-left.text-gray::text').get()
        wine_item["discount_percentage"] = None
        # TODO calculate
        wine_item["awards"] = []
        # [
        #     {
        #         "critic": award.css("strong ::text").get(),
        #         "score":   award.css("em ::text").get()
        #     } for award in awards
        # ]
        # TODO add playwright click
        wine_item["availability"] = None

        wine_item["appellation"] = response.xpath(
            '//h3[contains(text(), "Denominazione")]/following-sibling::div/text()').get()
        wine_item["grape_variety"] = response.xpath(
            '//h3[contains(text(), "Vitigni")]/following-sibling::div/text()').get()
        wine_item["alcohol_content"] = response.xpath(
            '//h3[contains(text(), "Gradazione alcolica")]/following-sibling::div/text()').get()
        # wine_item["serving_temperature"] = response.xpath(
        #     '//ul[@id="product-attribute-specs-table"]//strong[text()="Temperatura di servizio: "]/following-sibling::text()').get()
        # TODO add click
        wine_item["wine_type"] = response.xpath(
            '//h3[contains(text(), "Tipologia")]/following-sibling::div/a/text()').get()

        # # vivino_data = make_vivino_request(wine_item["name"])

        # # wine_item["vivino_rating"] = vivino_data.get('vivino_rating')
        # # wine_item["vivino_reviews"] = vivino_data.get('vivino_reviews')
        # # wine_item["vivino_url"] = vivino_data.get('vivino_url')
        # # wine_item["rating_source"] = vivino_data.get('source')
        yield wine_item
#         wines: SelectorList = response.css('article.productItem.productItem--standard')
#         for wine in wines:
#             wine_page_url = wine.css("div.productItem__info a::attr(href)").get()
# # response.xpath('//div[@class="c-productBox__image relative"]/a/@href').get()
