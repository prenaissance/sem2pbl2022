import json
import pymongo


class Category:
    def __init__(self, id, name, denom):
        self.id = id
        self.name = name
        self.denom = denom


def create_records(data):
    col.insert_one(data)


file = open('jobs.json')
data = json.load(file)
t = 0
i = 0

subcategories = []
c = {}

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["PBL"]
col = db["Subcategories"]

for j in data:
    t = 0

    for a in subcategories:
        if a["name"] == j["subcategory"]:
            t += 1
            break

    if t == 0:
        c = Category(i, j["subcategory"], 'A' + str(i)).__dict__
        print(c)

    if t == 0 and c["name"] != "other" and c["name"] != "missing" and c["name"] != "services":
        create_records(c)
        i += 1
        subcategories.append(c)
