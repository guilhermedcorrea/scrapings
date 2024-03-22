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


#driver.get("https://www.rocaceramica.com.br/produtos/")



list_products = []
dados = pd.read_excel(r"D:\scrapings_portobello\urls_roca_ceramica.xlsx")
urls = dados.to_dict(orient='records')

for url in urls:
    print(url["url"])

    driver.get(url["url"])
    print(url["description"])

    dict_product = {}

    driver.implicitly_wait(3)

    try:
        name = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[2]/div[1]/div/h2')[0].text
        dict_product["name"] = name
      
    except:
        pass

    try:
        product_type = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[2]/div[1]/div/div[1]/div[1]')[0].text
        dict_product["type"] = product_type
        
    except:
        pass

    try:
        reference = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[2]/div[1]/div/div[1]/div[2]')[0].text
        dict_product["reference"] = reference.split(":")[-1].strip()
        
    except:
        pass


    try:
        line = driver.find_elements(By.XPATH,'/html/body/section[1]/div/h1')[0].text
        dict_product["line"] = line
    except:
        pass

  
    images = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[1]/div/div[2]/div[1]/div/img')
    imgcont = 0
    for image in images:
        dict_product["image"+str(imgcont)] = image.get_attribute("src")
        imgcont +=1
       

    references = driver.find_elements(By.XPATH,"//div[@class='produto-label']")

    values = driver.find_elements(By.XPATH,"//div[@class='produto-info']")
    cont = 0
    for reference in references:
        dict_product[reference.text] = values[cont].text
        cont+=1
       
    
  
    especifications = driver.find_elements(By.XPATH, '/html/body/section[3]/div/div/table/tbody/tr/td')

   
    specifications_dict = {}

    
    for i in range(0, len(especifications), 2):
        key = especifications[i].text.strip() 
        value = especifications[i + 1].text.strip()
        specifications_dict[key] = value


    dict_product.update(specifications_dict)

    print(dict_product)
    list_products.append(dict_product)


dados = pd.DataFrame(list_products)
dados.to_excel("produtos_roca_ceramica.xlsx")

