from bs4 import BeautifulSoup
import requests
import pymysql
import time
import re
# import Comment

from accounts import *

crawlURL = "https://www.benedu.co.kr/Views/00_Common/99_BeneduQuestion.aspx?qst_id="

conn = pymysql.connect(host=sql_ip, port=3306, user=sql_user, password=sql_pw, database='benedu')
cursor = conn.cursor()
# sql = "SELECT * FROM answerSheet_2;"
# cursor.execute("sql")
# rows = cursor.fetchall()
# sql = "INSERT INTO answerSheet(qid,qans) VALUES(%s,%s)"
# cursor.execute(sql, dbtuple)

# logFile = open("log.txt", "w")  # not for this script


def requestbenedu(index):
    global elapTime
    requrl = crawlURL + str(index)
    req = requests.get(requrl)

    while req.status_code != 200:  # Error
        errorloop = 1
        req = requests.get(requrl)
        if errorloop >= 5:  # Repeated errors
            print("==============================")
            print("ERROR: status_code: " + req.status_code)
            print("URL: " + requrl + "\n")
            break

    reqtext = req.text
    reqheaders = req.headers
    reqstatus = req.status_code
    reqok = req.ok

    if len(req.text) <= 4000:  # no data
        print("Index " + str(index) + " no data")
        return

    soup = BeautifulSoup(reqtext, "html.parser")
    parsetext = str(soup)
    if parsetext.find("body") == -1:  # string format error
        print("Index " + str(index) + " no data")
        return


loop = 1
reqId = 1

# global var declaration
elapTime = 0.0

while 1:
    start_time = time.time()
    requestbenedu(reqId)
    reqId += 1
    elapTime = time.time() - start_time
    print("--- %d milliseconds --- \n\n" % (elapTime*1000))
    time.sleep(0.01)
