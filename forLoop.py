import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
from pyfcm import FCMNotification
import json
import pymongo

#connecting to the MongoDb
client = MongoClient()
database = client.smit

def insert(header,case_number,date_delivered,judge,court,parties,citation,case_content,category,collection):
    result = database[collection].insert_one(
        {
            "header": header,
            "case_number": case_number,
            "date_delivered": date_delivered,
            "date": datetime.strptime(date_delivered, '%d %b %Y'),
            "judge": judge,
            "court": court,
            "parties": parties,
            "citation": citation,
            "case_content": case_content,
            "category": category,
            "status": "pending"
        }
    )

    return result

def connect(url,category,collection):
    i=1
    connection = requests.get(url)
    soup = BeautifulSoup(connection.text, 'lxml')

    # post is the class of every case
    tag = soup.find("div", {"class": "post"})

    header = tag.find("h2").get_text()

    rows = tag.find_all("tr")
    metadata = rows[1].find_all("td")
    case_number = metadata[0].get_text().replace("Case Number:", "").strip(" ")
    date_delivered = metadata[1].get_text().replace("Date Delivered:", "").strip(" ")

    cursor = database.judgement.find(
        {"case_number": case_number, "date": datetime.strptime(date_delivered, '%d %b %Y')})

    if cursor.count() != 0:
        print("Stored")
        exit()
    else:
        print("Not Stored")

        paragraphs = tag.find_all("p")
        judge = paragraphs[0].get_text().replace("Judge:", "").strip(" ")
        court = paragraphs[1].get_text().replace("Court:", "").strip(" ")
        parties = paragraphs[2].get_text().replace("Parties:", "").strip(" ")
        citation = header

        link_tag = tag.find("a", {"class": "show-more"})
        link_of_article = link_tag['href']

        # connecting to the case
        case = requests.get(link_of_article)
        case_soup = BeautifulSoup(case.text, 'lxml')

        # judgement is the class of every case details
        case_details = case_soup.find("div", {"class": "judgement"})
        case_content = case_details.find("div", {"class": "case_content"}).get_text()

        result = insert(header,case_number,date_delivered,judge,court,parties,citation,case_content,category,collection)

        print(i)
        print(category)

connect("http://kenyalaw.org/caselaw/cases/actions/1/","judgement","judgement")
connect("http://kenyalaw.org/caselaw/cases/actions/2/","ruling","ruling")