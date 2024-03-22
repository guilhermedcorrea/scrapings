from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)


list_products = []
dados = pd.read_excel(r"D:\scrapings_portobello\urls_decorstile.xlsx")
urls = dados['urls'].to_list()
for url in urls:
    driver.get(url)
    time.sleep(2)
    
    dict_product = {}

    try:
        dict_product["url"] = url
    except:
        pass

    try:
        name = driver.find_elements(By.XPATH,'/html/body/main/section/div/div/div[2]/div[1]/div[1]/h2')[0].text
        print(name)
        dict_product["name"] = name
    except:
        pass

    try:
        dimension = driver.find_elements(By.XPATH,'/html/body/main/section/div/div/div[2]/div[1]/div[1]/h3')[0].text
        print(dimension)
        dict_product["dimension"] = dimension
    except:
        pass

    try:
        description = driver.find_elements(By.XPATH,'/html/body/main/section/div/div/div[2]/div[1]/div[2]/p')[0].text
        print(description)
        dict_product["description"] = description
    except:
        pass

    keys = driver.find_elements(By.XPATH,'/html/body/main/section/div/div/div[2]/div[1]/div[3]/ul/li/h4')
    
    values = driver.find_elements(By.XPATH,'/html/body/main/section/div/div/div[2]/div[1]/div[3]/ul/li/p')
    cont = 0
    for key in keys:
        dict_product[key.text] = values[cont].text
        cont+=1

   
    try:
        imagem = driver.find_elements(By.XPATH,'/html/body/main/section/div/div/div[1]/div[1]/div[1]/div/div[1]/div/div[1]/a/img')
        for img in imagem:
            dict_product["image"] = img.get_attribute("src")
        
    except:
        pass
    
   
    print(dict_product)
    list_products.append(dict_product)


dados = pd.DataFrame(list_products)
dados.to_excel("produtos_decortiles.xlsx", index=False)

