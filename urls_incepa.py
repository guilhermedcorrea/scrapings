
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)

driver.get("https://www.incepa.com.br/produtos/")


driver.implicitly_wait(10)


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


categories = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div/a")
for category in categories:
    print(category.get_attribute("href"))
    list_categories.append(category.get_attribute("href"))


for lista in list_categories:
    driver.get(lista)

    url_description = {}

    driver.implicitly_wait(10)

    try:
        description_lines = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[2]/div[2]/p')[0].text
        print(description_lines)
        url_description["desciption"] = description_lines
    except:
        pass

    products = driver.find_elements(By.XPATH,'/html/body/section/div/div/a')
    for product in products:
        print(product.get_attribute("href"))
        url_description["url"] = product.get_attribute("href")


    list_dict_url.append(url_description)


dados = pd.DataFrame(list_dict_url)
dados.to_excel("urls_incepa.xlsx")

for listas in list_dict_url:
   

    driver.get(listas["url"])

    driver.implicitly_wait(10)

    try:
        name = driver.find_elements("/html/body/div[5]/div/div[1]/div/h2")[0].text
        print(name)
    except:
        pass


    try:
        product_type = driver.find_elements("/html/body/div[5]/div/div[1]/div/div[1]")[0].text
        print(product_type)
    except:
        pass

    try:
        product_reference = driver.find_elements("/html/body/div[5]/div/div[1]/div/div[2]")[0].text
        print(product_reference)
    except:
        pass


