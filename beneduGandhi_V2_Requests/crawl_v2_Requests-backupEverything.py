from bs4 import BeautifulSoup
import requests
import pymysql
import time

from accounts import *

crawlURL = "https://www.benedu.co.kr/Views/00_Common/99_BeneduQuestion.aspx?qst_id="

conn = pymysql.connect(host=sql_ip, port=3306, user=sql_user, password=sql_pw, database='benedu')
cursor = conn.cursor()


def requestbenedu(index):
    global elapTime
    requrl = crawlURL + str(index)
    req = requests.get(requrl)

    while req.status_code != 200 or req.ok == False:  # Error
        errorloop = 1
        req = requests.get(requrl)
        if errorloop >= 5:  # Repeated errors
            print("==============================")
            print("ERROR: status_code: " + req.status_code)
            print("URL: " + requrl + "\n")
            break

    print("Index " + str(index) + " response OK")

    parsetext = str(BeautifulSoup(req.text, "html.parser"))

    if len(req.text) <= 4000 or parsetext.find("body") == -1:  # no data
        print("Index " + str(index) + " NO-DATA")
        dataok = 0
    else:
        print("Index " + str(index) + " data OK")
        dataok = 1

    if index >= 30000 and len(req.text) <= 3090:
        time.sleep(0.5)
        return

    try:
        sql = """INSERT INTO beneduBackup (qid, text, dataOK) VALUES(%s, %s, %s)"""
        cursor.execute(sql, (str(index), parsetext, dataok))
        conn.commit()
    except UnicodeEncodeError:
        dataok = 0
        print("Index " + str(index) + " EncodingError")
        sql = """INSERT INTO beneduBackup (qid, text, dataOK) VALUES(%s, %s, %s)"""
        cursor.execute(sql, (str(index), "UnicodeEncodeError", dataok))
        conn.commit()


# global var declaration
loop = 1
reqId = 43252636514632
elapTime = 0.0

while 1:
    print("\n------ Index ", reqId, " ------")
    start_time = time.time()
    requestbenedu(reqId)
    reqId += 1
    elapTime = time.time() - start_time
    print("--- %d milliseconds ---" % (elapTime*1000))
    time.sleep(0.01)
