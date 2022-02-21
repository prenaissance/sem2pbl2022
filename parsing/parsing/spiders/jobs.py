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

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    #allowed_domains = ['999.md/ro/']
    base_url="https://999.md"
    url = 'https://999.md/ro/category/work'
    cookieJar={
        "show_all_checked_childrens":	"no",
        #"selected_currency":            "usd",
        "hide_duplicates":          	"yes",
        "simpalsid.lang":              	"ro",
        "view_type":                	"detail",
    }

    def parse_category(self, response):
        link_list=response.css(".category__subCategories-collection a::attr(href)").getall()
        for link in link_list:
            yield scrapy.Request(self.base_url+link,cookies=self.cookieJar,callback=self.parse_subcategory)
    
    def parse_subcategory(self, response):
        last_page=response.css(".is-last-page a::attr(href)").get()#link to lp
        curr_page=response.css(".current a::attr(href)").get()[:-7]
        if last_page:#more than 1 page
            pages=int(last_page[last_page.find("page=")+5:])
            for i in range(1,pages+1):
                yield scrapy.Request(self.base_url+curr_page+f"&page={i}",cookies=self.cookieJar,callback=self.parse_subcategory_items)
        else:
            yield scrapy.Request(self.base_url+curr_page,cookies=self.cookieJar,callback=self.parse_subcategory_items)#parse same page again
        

    def parse_subcategory_items(self, response):
        all_items=response.css("#js-ads-container.items__list__container")
        #curr_page=response.css(".current a::attr(href)").get()[:-7]
        #category,subcategory=curr_page.split("/")[3:5]
        #subcategory=subcategory[:subcategory.find("?")]
        links= all_items.css(".ads-list-table-title-wrapper a::attr(href)")
        for link in links:
            yield scrapy.Request(self.base_url+link,cookies=self.cookieJar,callback=self.parse_job)

    def parse_job(self, response):
        ad=response.css(".adPage.cf")
        views=ad.css(".adPage__aside__stats__views::text").get()
        l={
            "name":ad.css(".adPage__header h1::text").get(),
            "price":ad.css(".adPage__content__features__value::text").get(),#different currencies
            "viewsAll":views[13:views.find("(")],
            "viewsToday":views[views.find("(astăzi ")+8:-1]
            #don't think that description is important, we might add it later

        }
        yield l
        

    def start_requests(self):#override default to add currency cookies
        url=self.url
        request=scrapy.Request(url,cookies=self.cookieJar,callback=self.parse_category)
        return [request]
