import scrapy


class ModelSpider(scrapy.Spider):
    name = 'model'
    allowed_domains = ['https://999.md/ro/list/computers-and-office-equipment/video']
    start_urls = ['http://https://999.md/ro/list/computers-and-office-equipment/video/']

    def parse(self, response):
        pass
