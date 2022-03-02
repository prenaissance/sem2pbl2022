import json
import pymongo
import time


class Record:
    def __init__(self, subcategory, avg_income, views_td, views_all):
        self.subcategory = subcategory
        self.avg_income = avg_income
        self.views_td = views_td
        self.views_all = views_all
        self.last_updated = time.ctime(time.time())


class DataToCalc:
    a = 0

    def __init__(self, subcategory, avg_income, views1, views2):
        self.subcategory = subcategory
        self.avg_income = avg_income
        self.views1 = views1
        self.views2 = views2
        self.a = 1

    def update(self, avg_income, v1, v2):
        self.avg_income += avg_income
        self.views1 += v1
        self.views2 += v2
        self.a += 1

    def calculate_avg(self):
        self.avg_income = round(self.avg_income / self.a)


def create_record(data):
    col2.insert_one(data)


def update_records(data):
    for i in data:
        query = {"subcategory": i["subcategory"]}
        values = {"$set": {"avg_income": i["avg_income"], "views_td": i["views_td"],
                           "views_all": i["views_all"], "last_updated": i["last_updated"]}}

        col2.update_one(query, values)


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["PBL"]
col1 = db["Subcategories"]
col2 = db["Main"]

file = open('jobs.json')
data = json.load(file)

records = []
nums = []
categories = []
cat = {}
rec = {}
i = 0


for i in data:
    t = 0

    for j in nums:
        if j.subcategory == i["subcategory"]:
            t = 1
            break

    money = i["priceValue"]

    if i["priceCurrency"] != "lei":
        money = money * 19

    if t == 0:
        inc = DataToCalc(i["subcategory"], money, i["viewsToday"], i["viewsAll"])
        nums.append(inc)

    elif t == 1:
        for j in nums:
            if j.subcategory == i["subcategory"]:
                j.update(money, i["viewsToday"], i["viewsAll"])
                break

x = col1.find()

for i in x:
    cat = {"name": i["name"], "id": i["id"]}
    categories.append(cat)

for j in nums:
    t = 0
    j.calculate_avg()

    for i in categories:
        if i["name"] == j.subcategory:
            rec = Record(i["id"], j.avg_income, j.views1, j.views2).__dict__

    x = col2.find()

    for i in x:
        if i["subcategory"] == rec["subcategory"]:
            records.append(rec)
            t = 1
            break

    if t == 0:
        create_record(rec)

update_records(records)
