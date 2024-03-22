from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver = webdriver.Chrome(options=options)


driver.get("https://www.rocaceramica.com.br/produtos/")



def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



list_categories = []
list_dict_url = []
while True:
    old_scroll_position = driver.execute_script("return window.pageYOffset;")
    scroll_to_bottom()
    driver.implicitly_wait(2) 
    new_scroll_position = driver.execute_script("return window.pageYOffset;")
    if new_scroll_position == old_scroll_position:
        break


categories = driver.find_elements(By.XPATH, "/html/body/section[2]/div/div/div/div/a")
for category in categories:
    print(category.get_attribute("href"))
    list_categories.append(category.get_attribute("href"))


for lista in list_categories:
    driver.get(lista)
    dict_descriptiobns = {}

    driver.implicitly_wait(7)

    try:
        description = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div/div/p')[0].text
        print(description)
        dict_descriptiobns["description"] = description
    except:
        pass

    urls = driver.find_elements(By.XPATH,'/html/body/section[3]/div/div/a')
    for url in urls:
        dict_descriptiobns["url"] = url.get_attribute("href")
        print(url.get_attribute("href"))
        list_dict_url.append(dict_descriptiobns)


dados = pd.DataFrame(list_dict_url)
dados.to_excel("urls_roca_ceramica.xlsx")