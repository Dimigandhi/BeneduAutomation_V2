from bs4 import BeautifulSoup
import requests
import pymysql
import time

from accounts import *

crawlURL = "https://www.benedu.co.kr/Views/00_Common/99_BeneduQuestion.aspx?qst_id="

conn = pymysql.connect(host=sql_ip, port=3306, user=sql_user, password=sql_pw, database='benedu')
cursor = conn.cursor()
# sql = "SELECT * FROM answerSheet_2;"
# cursor.execute("sql")
# rows = cursor.fetchall()
# sql = "INSERT INTO answerSheet(qid,qans) VALUES(%s,%s)"
# cursor.execute(sql, dbtuple)


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

    sql = """INSERT INTO beneduBackup (qid, text, dataOK) VALUES(%s, %s, %s)"""
    cursor.execute(sql, (str(index), parsetext, dataok))
    conn.commit()

    pass


loop = 1
reqId = 1

# global var declaration
elapTime = 0.0

while 1:
    print("\n------ Index ", reqId, " ------")
    start_time = time.time()
    requestbenedu(reqId)
    reqId += 1
    elapTime = time.time() - start_time
    print("--- %d milliseconds ---" % (elapTime*1000))
    time.sleep(0.01)
