from urllib.request import Request
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

class JobsFastSpider(scrapy.Spider):
    name = 'jobsFast'
    #allowed_domains = ['999.md/ro/']
    base_url="https://999.md"
    url = 'https://999.md/ro/category/services'
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
        curr_page=response.url+"?view_type=detail"
        if last_page:#more than 1 page
            pages=int(last_page[last_page.find("page=")+5:])
            pages=pages if pages<=5 else 5
            for i in range(1,pages+1):
                yield scrapy.Request(curr_page+f"&page={i}",cookies=self.cookieJar,callback=self.parse_subcategory_items)
        else:
            yield scrapy.Request(curr_page,cookies=self.cookieJar,callback=self.parse_subcategory_items)#parse same page again
        

    def parse_subcategory_items(self, response):
        all_items=response.css("#js-ads-container .ads-list-detail-item")
        curr_page=response.css(".items__header__store .is-active a::attr(href)").get()
        filtered_items=filter(filterItems,all_items)
        
        for item in filtered_items:
            yield scrapy.Request(self.base_url+item.css(".ads-list-detail-item-title a::attr(href)").get(),cookies=self.cookieJar,callback=self.parse_job)


    def parse_job(self, response):
        link=response.url
        price=response.css(".adPage__content__price-feature__prices__price.is-main")
        priceValue=int(parsePrice(price.css(".adPage__content__price-feature__prices__price__value::attr(content)").get()))
        priceCurrency=price.css(".adPage__content__price-feature__prices__price__currency::attr(content)").get()
        name=response.css(".adPage__header h1::text").get()
        viewsText=response.css(".adPage__aside__stats__views::text").get()
        viewsAll=int(parsePrice(viewsText[viewsText.find(":")+2:viewsText.find("(")-1]))
        viewsToday=int(parsePrice(viewsText[viewsText.find("(")+8:viewsText.find(")")]))
        category,subcategory=response.css("#m__breadcrumbs li a")[1:3].css("::attr(href)").getall()
        category=category.split("/")[-1]
        subcategory=subcategory.split("/")[-1]

        l={
            "name":name,
            "priceValue":priceValue,
            "priceCurrency":priceCurrency,
            "viewsToday":viewsToday,
            "viewsAll":viewsAll,
            "category":category,
            "subcategory":subcategory,
            "link":link
        }
        yield l

    def start_requests(self):#override default to add currency cookies
        url=self.url
        request=scrapy.Request(url,cookies=self.cookieJar,callback=self.parse_category)
        
        return [request]
