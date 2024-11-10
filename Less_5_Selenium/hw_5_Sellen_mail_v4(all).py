import wait as wait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pprint import pprint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions as se
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


client = MongoClient('127.0.0.1', 27017)
db = client['letters']
letters = db.email

# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172???

driver = webdriver.Chrome(executable_path='C:/chromedriver.exe')
driver.get('https://mail.ru')

login = 'study.ai_172@mail.ru'
password = 'NextPassword172???'

chrome_options = Options()
wait = WebDriverWait(driver, 10)

all_emails = []
links_list = []

def autorisation(login, password):
    # функция авторизации
    elem = driver.find_element_by_xpath("//input[@class='email-input svelte-1tib0qz']")
    elem.send_keys(login)
    elem.send_keys(Keys.ENTER)               # нажатие кнопки
    elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'password-input'))) # ожидание
    elem.send_keys(password)
    elem.send_keys(Keys.ENTER)               # нажатие кнопки
    return

autorisation(login, password)

def get_link_letters():
    '''собираю линки по всем письмам '''
    links = []
    while True:
        try:
            items = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div/a[contains(@class, 'llc')]")))
            for item in items:
                links.append(item.get_attribute('href'))
            item.send_keys(Keys.PAGE_DOWN)
            # time.sleep(1)
            time.sleep(0.5)
        except se.ElementNotInteractableException:
            break
    links = set(links)
    return links


def get_emails(url_email):
  # '''получим инфориацию по имейлам
  #  и добавим в БД '''
    url_email = list(url_email)
    for i in url_email:
        driver.get(i)
        # time.sleep(1)
        time.sleep(0.5)
        email_info = {}
        try:
            subject = (driver.find_element_by_xpath("//h2[@class='thread__subject']")).text
        except:
            subject = None
        try:
            date = (driver.find_element_by_xpath("//div[@class='letter__date']")).text
        except:
            date = None
        try:
            author = (driver.find_element_by_xpath("//span[@class='letter-contact']")).text
        except:
            author = None
        try:
            text = (driver.find_element_by_xpath("//div[@class='letter__body']")).text
        except:
            text = None

        email_info['subject'] = subject
        email_info['date'] = date
        email_info['author'] = author
        email_info['text'] = text
        all_emails.append(email_info)

        try:
            letters.insert_one({'_id': i,
                                  'subject': subject,
                                  'date': date,
                                  'author': author,
                                  'text': text
                                  })
        except dke:
            continue

    return all_emails

links_email = get_link_letters()
get_emails(links_email)
pprint(len(links_email))
