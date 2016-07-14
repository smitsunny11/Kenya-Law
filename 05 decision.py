"""

@Author : Smit Shah <smitsunny11@gmail.com
@Last_Modified : 23/6/16
@Purpose : Scraping Data From kenyalaw.org and storing it in MongoDB Database

"""

#imports

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

#connecting to the MongoDb
client = MongoClient()
database = client.smit

#i=1
#connecting to the site
name = "http://kenyalaw.org/caselaw/cases/actions/5/"
connection = requests.get(name)
soup = BeautifulSoup(connection.text, 'lxml')

#post is the class of every case
tags = soup.find_all("div", {"class": "post"})


for tag in tags:
    header = tag.find("h2").get_text()

    rows = tag.find_all("tr")
    metadata = rows[1].find_all("td")
    case_number = metadata[0].get_text().replace("Case Number:","").strip(" ")
    date_delivered = metadata[1].get_text().replace("Date Delivered:","").strip(" ")

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
    result = database.decision.insert_one(
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
            "category" : "decision",
            "status" : "sent"
        }
    )



    #print(i)
    #i=i+1




