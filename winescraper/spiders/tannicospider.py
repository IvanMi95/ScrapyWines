from scrapy import Request, Spider

from winescraper.items import WineItem
from winescraper.util.util import custom_print
from winescraper.util.vivino_util import construct_vivino_query, make_vivino_request
# scrapy crawl tannicospider
# xpath other method

# <script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>
# <style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>
# <svg\b[^<]*(?:(?!<\/svg>)<[^<]*)*<\/svg>
# ^\s*$\n
# <!--[\s\S]*?-->


class TannicoSpider(Spider):
    name = "tannicospider"
    allowed_domains = ["www.tannico.it", "www.vivino.com"]
    start_urls = ["https://www.tannico.it/vini/vini-bianchi-in-offerta.html"]
    # start_urls = ["https://www.tannico.it/vini/vini-rossi-in-offerta.html"]

    def parse(self, response):
        wines = response.css('article.productItem.productItem--standard')

        for wine in wines:
            wine_page_url = wine.css("div.productItem__info a::attr(href)").get()
            yield response.follow(wine_page_url, callback=self.parse_wine, meta={'wine_page_url': wine_page_url})

    def parse_wine(self, response):
        wine_item = WineItem()

        old_prices = response.css('span.price::text')
        awards = response.css('ul.productItem__awards.productItem__awards--large li span')

        wine_item["name"] = response.css('div.productPage__content h1 ::text').get()
        wine_item["url"] = response.meta['wine_page_url']
        wine_item["sale_price"] = response.css('span.new-price::text').get()
        wine_item["original_price"] = old_prices[0].get() if len(old_prices) > 0 else None
        wine_item["lowest_price"] = old_prices[1].get() if len(old_prices) > 1 else None
        # wine_item["discount_percentage"] = response.css(
        #     'span.perliter-price.omnibus-discount-label::text').get()
        wine_item["awards"] = [
            {
                "critic": award.css("strong ::text").get(),
                "score":   award.css("em ::text").get()
            } for award in awards
        ]
        wine_item["availability"] = response.xpath(
            '//ul[@id="product-attribute-delivery"]//li[@class="special"]/p/span/text()').get()
        wine_item["appellation"] = response.xpath(
            '//ul[@id="product-attribute-specs-table"]//strong[text()="Denominazione: "]/following-sibling::text()').get()
        wine_item["grape_variety"] = response.xpath(
            '//ul[@id="product-attribute-specs-table"]//strong[text()="Vitigni: "]/following-sibling::text()').get()
        wine_item["alcohol_content"] = response.xpath(
            '//ul[@id="product-attribute-specs-table"]//strong[text()="Alcol: "]/following-sibling::text()').get()
        wine_item["serving_temperature"] = response.xpath(
            '//ul[@id="product-attribute-specs-table"]//strong[text()="Temperatura di servizio: "]/following-sibling::text()').get()
        wine_item["wine_type"] = response.xpath(
            '//ul[@id="product-attribute-specs-table"]//strong[text()="Tipologia: "]/following-sibling::text()').get()

        vivino_data = make_vivino_request(wine_item["name"])

        wine_item["vivino_rating"] = vivino_data.get('vivino_rating')
        wine_item["vivino_reviews"] = vivino_data.get('vivino_reviews')
        wine_item["vivino_link"] = vivino_data.get('vivino_link')
        yield wine_item
