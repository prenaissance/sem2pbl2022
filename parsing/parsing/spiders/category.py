import scrapy
from ..items import ParsingItem
#from scrapy.loader import ItemLoader 
import json
import re

def filterItems(item):#filter ads, negotiable items and buy offers (worst people post there)
    if (item.css(".figure.figure--booster-small").get()
        or item.css(".ads-list-detail-item-price-wrapper::text").get()=="  negociabil  "
        or item.css(".is-offer-type").get()):
        return False
    return True

def parsePrice(price):#removes all non-numbers
    return re.sub(r"[^0-9]","",price)

class CategorySpider(scrapy.Spider):
    name = 'category'
    #allowed_domains = ['999.md/ro/']
    base_url="https://999.md"
    url = 'https://999.md/ro/category/computers-and-office-equipment'
    cookieJar={
        "show_all_checked_childrens":	"no",
        "selected_currency":            "usd",
        "hide_duplicates":          	"yes",
        "simpalsid.lang":              	"ro",
        "view_type":                	"detail",
    }

    def parse(self, response):
        pass#for now

    def parse_category(self, response):
        link_list=response.css(".category__subCategories-collection a::attr(href)").getall()
        for link in link_list:
            yield scrapy.Request(self.base_url+link,cookies=self.cookieJar,callback=self.parse_subcategory)
    
    def parse_subcategory(self, response):
        last_page=response.css(".is-last-page a::attr(href)").get()#link to lp
        curr_page=response.css(".items__header__store .is-active a::attr(href)").get()+"?view_type=detail"
        if last_page:#more than 1 page
            pages=int(last_page[last_page.find("page=")+5:])
            for i in range(1,pages+1):
                yield scrapy.Request(self.base_url+curr_page+f"&page={i}",cookies=self.cookieJar,callback=self.parse_subcategory_items)
        else:
            yield scrapy.Request(self.base_url+curr_page,cookies=self.cookieJar,callback=self.parse_subcategory_items)#parse same page again
        

    def parse_subcategory_items(self, response):
        all_items=response.css("#js-ads-container .ads-list-detail-item")
        curr_page=response.css(".items__header__store .is-active a::attr(href)").get()
        category,subcategory=curr_page.split("/")[3:5]
        subcategory=subcategory[:subcategory.find("?")]
        filtered_items=filter(filterItems,all_items)
        for item in filtered_items:
            l={
                "category":category,
                "subcategory":subcategory,
                "name":item.css(".ads-list-detail-item-title a::text").get(),
                "price":parsePrice(item.css(".ads-list-detail-item-price-wrapper::text").get())
                #don't think that description is important, we might add it later

            }
            yield l
        

    def start_requests(self):#override default to add currency cookies
        url=self.url
        request=scrapy.Request(url,cookies=self.cookieJar,callback=self.parse_category)
        #request=scrapy.Request("https://999.md/ro/list/computers-and-office-equipment/keyboards-mice-joysticks?store=?view_type=detail",
        #cookies=self.cookieJar,callback=self.parse_subcategory_items)
        return [request]
