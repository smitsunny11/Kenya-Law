
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import pymongo
from pyfcm import FCMNotification
import json

#connecting to the MongoDb
client = MongoClient()
database = client.smit

notification_count = 0

#connecting to the site

#----------------------------------------1 Judgement----------------------------------------------------------#
i = 1
name = "http://kenyalaw.org/caselaw/cases/actions/1/"
connection = requests.get(name)
soup = BeautifulSoup(connection.text, 'lxml')

#post is the class of every case
tag = soup.find("div", {"class": "post"})


header = tag.find("h2").get_text()

rows = tag.find_all("tr")
metadata = rows[1].find_all("td")
case_number = metadata[0].get_text().replace("Case Number:","").strip(" ")
date_delivered = metadata[1].get_text().replace("Date Delivered:","").strip(" ")

cursor = database.judgement.find({"case_number": case_number , "date":datetime.strptime(date_delivered,'%d %b %Y')})


if cursor.count() != 0:
    print("Stored")
    exit()
else:
    print("Not Stored")

    paragraphs = tag.find_all("p")
    judge = paragraphs[0].get_text().replace("Judge:","").strip(" ")
    court = paragraphs[1].get_text().replace("Court:","").strip(" ")
    parties = paragraphs[2].get_text().replace("Parties:","").strip(" ")
    citation = header

    link_tag = tag.find("a",{"class":"show-more"})
    link_of_article = link_tag['href']


    #connecting to the case
    case = requests.get(link_of_article)
    case_soup = BeautifulSoup(case.text, 'lxml')

    #judgement is the class of every case details
    case_details = case_soup.find("div", {"class": "judgement"})
    case_content = case_details.find("div", {"class": "case_content"}).get_text()

    #inserting into database
    result = database.judgement.insert_one(
        {
            "header" : header,
            "case_number" : case_number,
            "date_delivered" : date_delivered,
            "date" : datetime.strptime(date_delivered,'%d %b %Y'),
            "judge" : judge,
            "court" : court,
            "parties" : parties,
            "citation" : citation,
            "case_content" : case_content,
            "category" : "judgement",
            "status" : "pending"
        }
    )

    hase = database.judgement.find().sort('_id',pymongo.DESCENDING).limit(1)

    for a in hase:
        ida=a['_id']
        category=a['category']

    print(i)
    print(ida)
    print(category)
    i=i+1
    string = '{"id":"' + str(ida) + '","category":"' + str(category) + '"}'


    if notification_count < 2:

        # Send to single device.

        push_service = FCMNotification(api_key="AIzaSyBl6il28Gs0OeQGdzF4FsjRuaZoT6C8r38")

        regs = database.notification.find()
        id = database.judgement.find()
        registration_ids = []

        for reg in regs:
            registration_ids.append(reg['device_id'])
        message_title = header
        message_body = case_number
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=json.loads(string))
        print(string)
        print(result)
        notification_count = notification_count + 1
    else:
        exit()

"""
    # Send to multiple device.


    last_case = database.judgement.find().sort('_id',pymongo.DESCENDING).limit(1)
    for a in last_case:
        ida = a['_id']
        category = a['category']
    string = '{"id":"' + str(ida) + '","category":"' + str(category) + '"}'

    push_service = FCMNotification(api_key="AIzaSyBl6il28Gs0OeQGdzF4FsjRuaZoT6C8r38")
    regs = database.notification.find()
    registration_ids = []

    for reg in regs:
        registration_ids.append(reg['device_id'])
    message_title = header
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=json.loads(string))
    #          print(result)
    """

