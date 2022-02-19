# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from unicodedata import category
import scrapy


class ParsingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category=scrapy.Field()
    subcategory=scrapy.Field()
    name=scrapy.Field()
    price=scrapy.Field()#in usd
