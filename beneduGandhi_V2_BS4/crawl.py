from bs4 import BeautifulSoup
import requests, pymysql, time
# import Comment


sql_ip = '149.28.29.84'
sql_user = 'benedu_RW'
sql_pw = 'bendbpass!@'

crawlURL = "https://www.benedu.co.kr/Views/00_Common/99_BeneduQuestion.aspx?qst_id="

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


conn = pymysql.connect(host=sql_ip, port=3306, user=sql_user, password=sql_pw, database='benedu')
cursor = conn.cursor()
cursor.execute("SELECT * FROM answerSheet_2;")
rows = cursor.fetchall()
# sql = "INSERT INTO answerSheet(qid,qans) VALUES(%s,%s)"
# cursor.execute(sql, dbtuple)

file = open("log.txt", "w")


def requestBenedu(index):
    global elapTime
    reqURL = crawlURL + str(index)
    req = requests.get(reqURL)
    reqText = req.text
    reqHeaders = req.headers
    reqStatus = req.status_code
    reqOk = req.ok

    soup = BeautifulSoup(reqText, "html.parser")

    print("==============================")
    print("URL: " + reqURL)
    # print("Text: " + reqText)
    # print("Soup: " + str(soup))
    print("TextSize: " + str(len(reqText)))
    print("Headers: " + str(reqHeaders))
    print("Status: " + str(reqStatus))
    print("OK: " + str(reqOk))
    file.write("==============================\n")
    file.write("URL: " + reqURL + "\n")
    file.write("TextSize: " + str(len(reqText)) + "\n")
    file.write("Headers: " + str(reqHeaders) + "\n")
    file.write("Status: " + str(reqStatus) + "\n")
    file.write("OK: " + str(reqOk) + "\n")
    elapTime = time.time() - start_time
    file.write("--- %s seconds --- \n" % elapTime)
    file.write("Soup: " + str(soup) + "\n\n\n\n")


loop = 1
reqId = 1
elapTime = 0.0
while 1:
    start_time = time.time()
    requestBenedu(reqId)
    reqId += 1
    print("--- %s seconds --- \n\n" % elapTime)
    time.sleep(0.01)
