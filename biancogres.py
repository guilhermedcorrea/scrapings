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
driver.get("https://www.biancogres.com.br/pt_BR/produtos")

time.sleep(5)



lista_urls = []

load_button_count = len(driver.find_elements(By.XPATH,"//button[@class='products-gallery__load-button']"))

print("Número de botões 'Carregar mais produtos +':", load_button_count)

for i in range(1, load_button_count):
    button_xpath = f'//*[@id="top-page"]/section[2]/section[3]/div[{i}]/button'
    button = driver.find_element(By.XPATH, button_xpath)
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)
    print(i)

    products = driver.find_elements(By.XPATH,'//*[@id="top-page"]/section[2]/section[3]/div/div/a')
    for product in products:
        print(product.get_attribute("href"))
        lista_urls.append(product.get_attribute("href"))

    driver.execute_script("window.scrollTo(0, window.scrollY + 500);") 


    time.sleep(2)

lista_products = []
for lista in lista_urls:
    driver.get(lista)

    dict_products = {}
    try:
        dict_products["url"] = lista
    except:
        pass

    try:
        name = driver.find_elements(By.XPATH,'//*[@id="top-page"]/section[2]/section[1]/section/div[1]/h2')[0].text
        dict_products["name"] = name
    except:
        pass


    try:
        description = driver.find_elements(By.XPATH,'//*[@id="top-page"]/section[2]/section[1]/section/div[1]/p')[0].text
        dict_products["description"] = description
    except:
        pass


    try:
        images = driver.find_elements(By.XPATH,'//*[@id="top-page"]/section[2]/section[1]/section/div[2]/div/figure/div/div/div/img')
        imgcont = 0
        for image in images:
            dict_products["images"+str(imgcont)] = image.get_attribute("src").replace("thumb_240p.jpg","thumb_480p.jpg")
            imgcont +=1
    except:
        pass


    try:
        elements = driver.find_elements(By.XPATH, '//*[@id="top-page"]/section[2]/section[3]/div/section/ul/li/span')

        my_dict = {}

        for element in elements:
            
            parts = element.text.split('\n')
            
            key = parts[0]
            value = parts[-1]
            my_dict[key] = value
    except:
        pass

    dict_products.update(my_dict)

    print(dict_products)
    lista_products.append(dict_products)

dados = pd.DataFrame(lista_products)
dados.to_excel("produtos_biancogres.xlsx", index=False)


   
   



