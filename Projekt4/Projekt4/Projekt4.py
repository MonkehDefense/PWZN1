from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import sys

def main():
    if len(sys.argv) < 2:
        sys.exit('Nie podano nazwy pliku JSON do zapisu danych.')
    file=''
    if sys.argv[1][-5:] != '.json':
        file=sys.argv[1]+'.json'
    else: file=sys.argv[1]

    options = Options()
    #options.add_argument('--disable-notifications')
    #options.add_argument('--headless')
    
    service = Service('.\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://aminoapps.com/c/monster-hunter/recent/')
    
    posts = set()
    posts.update(set(driver.find_elements(By.XPATH,'/html/body/section/section/section/section/div/article/a/section/h3')))
    
    for i in range(20):
        time.sleep(3)
        #driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
        posts.update(set(driver.find_elements(By.XPATH,'/html/body/section/section/section/section/div/article/a/section/h3')))
    
    posts = [post.text for post in posts]
    driver.close()
    
    #print(posts)
    with open(file,'w', encoding='utf-8') as f:
        json.dump(posts,f)
    with open(file, 'r', encoding='utf-8') as f:
        print(json.load(f))

if __name__ == "__main__":
    main()