from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pymysql, random, time,re


indexURL = 'https://benedu.co.kr/Index.aspx'

sql_ip = '149.28.29.84'
sql_user = 'benedu_RW'
sql_pw = 'bendbpass!@'
conn = pymysql.connect(host=sql_ip, port=3306, user=sql_user, password=sql_pw, database='benedu')
cursor = conn.cursor()
###########새로운 DB로 수정 필요############
# answerSheet_2 테이블로 접속하면 됨


print("Benedu Email: ")
benID = input()
# benID = 'mamy0320@naver.com'
print("Benedu Password: ")
benPW = input()
for i in range(15):
    print()
print('------------------------------')
print()


NUMS_DICT = {
    "①" : 1,
    "②" : 2,
    "③" : 3,
    "④" : 4,
    "⑤" : 5
}


def login(benID, benPW):
    print()

    driver.get(indexURL)
    time.sleep(0.2)
    assert "No results found." not in driver.page_source

    driver.find_element_by_css_selector('#liLogin > a').click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#inputEmail')))
    time.sleep(0.2)
    driver.find_element_by_css_selector('#inputEmail').send_keys(benID)
    time.sleep(0.1)
    driver.find_element_by_css_selector('#inputPassword').send_keys(benPW)
    time.sleep(0.2)
    driver.find_element_by_css_selector('#btnLogin').click()
    time.sleep(0.2)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#mnu02StdGrade > a')))
    time.sleep(1.2)

    return

def getHoney():
    time.sleep(1)
    driver.find_element_by_css_selector('#mnu03StdStudy > a').click()
    time.sleep(0.1)
    driver.find_element_by_css_selector('#mnu03StdStudy > ul > li:nth-child(8) > a').click()
    time.sleep(0.5)
    return
#116703
def exScr(idx):
    driver.execute_script('ShowPop_My("'+str(idx)+'", "2018-12-07 18:12:56")')
    time.sleep(1.5)
    if(driver.current_url=="http://www.benedu.co.kr/errorStatus.aspx?aspxerrorpath=/Views/01_Students/03StdStudy07HoneyList.aspx"):
        print("err")
        driver.execute_script("window.history.go(-1)")
        return
    parseAns(idx)

def parseAns(idx):
    html = driver.page_source
    parpage = BeautifulSoup(html, 'html.parser')
    
    e = re.findall("(<p>[①②③④⑤]<\/p>)", str(parpage.find(id="text"))) 
    if(e):
        answer = NUMS_DICT[re.findall("[①②③④⑤]",e[0])[0]]
        if(answer):
            dbtuple = (idx,answer)
            print(dbtuple)
            # sql = "INSERT INTO answerSheet(qid,qans) VALUES(%s,%s)"
            # cursor.execute(sql, dbtuple)
            # conn.commit()
        return
    else:
        print(parpage.find(id="text"))
        return

driver = webdriver.Chrome('chromedriver.exe')
# driver.maximize_window()

login(benID, benPW)
getHoney()
counter = 116702
insertTotalDB = 0

while(1):   
    counter+=1
    print("index:  "+str(counter))
    time.sleep(1.5)
    exScr(counter)
    input()
