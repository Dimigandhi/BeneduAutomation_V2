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

logFile = open("log.txt", "w")

NUMS_DICT = {
    "①": 1,
    "②": 2,
    "③": 3,
    "④": 4,
    "⑤": 5,
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


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
            logFile.write("==============================")
            logFile.write("ERROR: status_code: " + req.status_code)
            logFile.write("URL: " + requrl + "\n")
            logFile.flush()
            break

    reqtext = req.text
    reqheaders = req.headers
    reqstatus = req.status_code
    reqok = req.ok

    if len(req.text) <= 4000:  # no data
        print("Index " + str(index) + " no data")
        logFile.write("Index " + str(index) + " no data")
        logFile.flush()
        return

    soup = BeautifulSoup(reqtext, "html.parser")
    parsetext = str(soup)
    if parsetext.find("body") == -1:  # string format error
        print("Index " + str(index) + " no data")
        logFile.write("Index " + str(index) + " no data")
        logFile.flush()
        return

    parsetext = parsetext[parsetext.find("body"):]
    parsetext = parsetext[:parsetext.find("/body")]
    parsetext = parsetext.replace(" ", "")
    parsetext = parsetext.replace("style", "")
    parsetext = parsetext.replace("=", "")
    parsetext = parsetext.replace("\"", "")
    parsetext = parsetext.replace("\n", "")
    parsetext = parsetext.replace("\r", "")
    parsetext = parsetext.replace("<span>", "")
    parsetext = parsetext.replace("</span>", "")
    parsetext = parsetext.replace(".", "")
    parsetext = parsetext.replace("&nbsp;", "")

    answer = patternsearch(parsetext)

    print("==============================")
    print("URL: " + requrl)
    if index == 1:
        print("Headers: " + str(reqheaders))
        print("Status: " + str(reqstatus))
        print("OK: " + str(reqok))
    print("TextSize: " + str(len(reqtext)))
    print("QID: " + str(index))
    if gotAns == 1:
        print("parseAnswer: " + str(parseAnswer))
        print("QAns: " + str(answer))
    if gotAns == 0:
        print("!!! Unable to find answer")
        print(parseAnswer)
        print(parsetext)

    logFile.write("==============================\n")
    logFile.write("URL: " + requrl + "\n")
    if index == 1:
        logFile.write("Headers: " + str(reqheaders) + "\n")
        logFile.write("Status: " + str(reqstatus) + "\n")
        logFile.write("OK: " + str(reqok) + "\n\n")
    logFile.write("TextSize: " + str(len(reqtext)) + "\n")
    logFile.write("QID: " + str(index) + "\n")
    if gotAns == 1:
        logFile.write("parseAnswer: " + str(parseAnswer) + "\n")
        logFile.write("QAns: " + str(answer) + "\n")
    if gotAns == 0:
        logFile.write("\n!!! Unable to find answer\n")
    logFile.flush()


def patternsearch(parsetext):
    global gotAns
    global parseAnswer
    answer = -1

    parseAnswer = re.findall("<p>[①②③④⑤]</p>", parsetext)  # list var
    if len(parseAnswer) == 0:
        parseAnswer = re.findall("<p>[①②③④⑤][^~]</p>", parsetext)
    if len(parseAnswer) == 0:
        parseAnswer = re.findall("<p>[^~][①②③④⑤]</p>", parsetext)
    if len(parseAnswer) == 0:
        parseAnswer = re.findall("\[[①②③④⑤]\]", parsetext)

    parseAnswer = re.findall("[①②③④⑤]", str(parseAnswer))

    if len(parseAnswer) == 1:  # 정상
        if "①" in parseAnswer:
            answer = 1
        elif "②" in parseAnswer:
            answer = 2
        elif "③" in parseAnswer:
            answer = 3
        elif "④" in parseAnswer:
            answer = 4
        elif "⑤" in parseAnswer:
            answer = 5

    # 문제번호도 인식하므로 2번씩 있는번호로
    if len(parseAnswer) == 6:
        if parseAnswer.count("①") == 2:
            answer = 1
        elif parseAnswer.count("②") == 2:
            answer = 2
        elif parseAnswer.count("③") == 2:
            answer = 3
        elif parseAnswer.count("④") == 2:
            answer = 4
        elif parseAnswer.count("⑤") == 2:
            answer = 5

    # 오답풀이 영역에서 없는번호로 선택
    if len(parseAnswer) == 0 or len(parseAnswer) == 4 or len(parseAnswer) == 9:
        parsetext = parsetext[parsetext.find("오답풀이"):]
        parseAnswer = re.findall("[①②③④⑤]", parsetext)
        if len(parseAnswer) > 0:
            if "①" not in parseAnswer:
                answer = 1
            elif "②" not in parseAnswer:
                answer = 2
            elif "③" not in parseAnswer:
                answer = 3
            elif "④" not in parseAnswer:
                answer = 4
            elif "⑤" not in parseAnswer:
                answer = 5

    gotAns = 1 if answer != -1 else 0
    return answer


loop = 1
reqId = 4087

# global var declaration
gotAns = 0
parseAnswer = ""
elapTime = 0.0

while 1:
    start_time = time.time()
    requestbenedu(reqId)
    reqId += 1
    elapTime = time.time() - start_time
    print("--- %d milliseconds --- \n\n" % (elapTime*1000))
    time.sleep(0.01)
