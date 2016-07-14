from pymongo import MongoClient
import pymongo
client = MongoClient()

database = client.smit

result = database.vinit.insert_one(
    {
        "header": "pankit",
        "case_number": "Smit",
        "date_delivered": "Vinit",
        "judge": "Vinit",
        "court": "Vinit",
        "parties": "Vinit",
        "citation": "Vinit",
        "case_content": "Vinit",
        "category": "judgement",
        "status": "sent"
    }
)

last_case = database["vinit"].find().sort('_id', pymongo.DESCENDING).limit(1)
for a in last_case:
    head = a['header']
print(head)
