import scrapy


class AsuraSpider(scrapy.Spider):
    name = "asura"
    allowed_domains = ["asuracomic.net"]
    start_urls = ["https://asuracomic.net"]

    def parse(self, response):
        pass
