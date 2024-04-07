import scrapy


class JpBoxSpider(scrapy.Spider):
    name = "jp_box"
    allowed_domains = ["site.com"]
    start_urls = ["https://site.com"]

    def parse(self, response):
        pass
