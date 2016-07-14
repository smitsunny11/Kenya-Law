"""

@Author : Smit Shah <smitsunny11@gmail.com
@Last_Modified : 24/6/16
@Purpose : Cron File

"""

#imports

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import pymongo
import os

#connecting to the MongoDb
client = MongoClient()
database = client.smit

notification_count = 0

#connecting to the site

#---------------------------------------Inserting Funcion --------------------------------------------------#

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


#--------------------------------------Connecting Function--------------------------------------------------#

def connect(url,category,collection):
    i=1
    connection = requests.get(url)
    soup = BeautifulSoup(connection.text, 'lxml')

    # post is the class of every case
    tags = soup.find_all("div", {"class": "post"})

    for tag in tags:
        header = tag.find("h2").get_text()

        rows = tag.find_all("tr")
        metadata = rows[1].find_all("td")
        case_number = metadata[0].get_text().replace("Case Number:", "").strip(" ")
        date_delivered = metadata[1].get_text().replace("Date Delivered:", "").strip(" ")

        cursor = database[collection].find(
            {"case_number": case_number, "date_delivered": date_delivered})

        if cursor.count() != 0:
            print("Stored")
            break
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

            # inserting into database
            result = insert(header, case_number, date_delivered, judge, court, parties, citation, case_content,category,collection)


            print(i)
            print(category)
            i=i+1

            if notification_count < 2:
                last_case = database[collection].find().sort('_id', pymongo.DESCENDING).limit(1)
                for a in last_case:
                    ida = a['_id']
                    cat = a['category']
                    head = a['header']
                global notification_count

                #Calling php file for sending notification
                string = "php /opt/lampp/htdocs/laravel/app/Console/Commands/send.php " + str(ida) + " " + str(cat) +" "+'"'+ str(head)+'"'
                os.system(string)

                notification_count=notification_count+1
            else:
                break







#----------------------------------------1 Judgement-------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/1/"
#connect(name,"judgement","judgement")

#----------------------------------------2 ruling----------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/2/"
#connect(name,"ruling","ruling")

#----------------------------------------3 Order-----------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/3/"
#connect(name,"order","order")

#----------------------------------------4 sentence--------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/4/"
#connect(name,"sentence","sentence")

#----------------------------------------5 decision--------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/5/"
#connect(name,"decision","decision")

#----------------------------------------6 objection-------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/6/"
connect(name,"objection","objection")

#----------------------------------------7 revision--------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/7/"
#connect(name,"revision","revision")

#----------------------------------------8 award-----------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/8/"
#connect(name,"award","award")

#----------------------------------------9 assessment------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/9/"
#connect(name,"assessment","assessment")

# ---------------------------------------10 directions-----------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/10/"
#connect(name,"directions","directions")

# ---------------------------------------11 advisory-------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/11/"
#connect(name,"advisory","advisory")

# ---------------------------------------12 summing--------------------------------------------------------#

#name = "http://kenyalaw.org/caselaw/cases/actions/12/"
#connect(name,"summing","summing")

# ---------------------------------------13 review---------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/13/"
#connect(name,"review","review")

# ---------------------------------------14 motion---------------------------------------------------------#

name = "http://kenyalaw.org/caselaw/cases/actions/14/"
#connect(name,"motion","motion")

# ---------------------------------------15 civil----------------------------------------------------------#

#name = "http://kenyalaw.org/caselaw/cases/actions/15/"
#connect(name,"civil","civil")

# ---------------------------------------16 criminal-------------------------------------------------------#

#name = "http://kenyalaw.org/caselaw/cases/actions/16/"
#connect(name,"criminal","criminal")