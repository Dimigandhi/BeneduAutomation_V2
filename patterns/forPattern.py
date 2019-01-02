from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pymysql, random, time,re




driver = webdriver.Chrome('chromedriver.exe')
# driver.maximize_window()

#1100~140 답안 x

counter = 1000
while(1):   
    driver.get('https://www.benedu.co.kr/Views/00_Common/99_BeneduQuestion.aspx?qst_id='+str(counter))
    if(input()=='b'):
        counter-=2
    counter+=1



