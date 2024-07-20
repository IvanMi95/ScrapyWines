import scrapy


class CallmewinespiderSpider(scrapy.Spider):
    name = "callmewinespider"
    allowed_domains = ["www.callmewine.com"]
    start_urls = ["https://www.callmewine.com"]

    def parse(self, response):
        pass
