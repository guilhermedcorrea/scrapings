from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)

#driver.get("https://www.incepa.com.br/produtos/")


#driver.implicitly_wait(10)

list_product = []

dados = pd.read_excel(r"D:\scrapings_portobello\urls_incepa.xlsx")
urls = dados.to_dict(orient='records')

for url in urls:
    driver.get(url['url'])

    dict_product = {}

    driver.implicitly_wait(7)
    print(url['desciption'])
    try:
        dict_product["description"] = url['desciption']
        dict_product["url"] = url['url']
    except:
        pass

    try:
        line = driver.find_elements(By.XPATH,'/html/body/section[1]/div/div/div/div/div/h1')[0].text
        
        dict_product["line"] = line
    except:
        pass

    try:
        name = driver.find_elements(By.XPATH,'/html/body/div[5]/div/div[1]/div/h2')[0].text
        dict_product["name"] = name
        
    except:
        pass
    
    try:
        product_type = driver.find_elements(By.XPATH,'/html/body/div[5]/div/div[1]/div/div[1]')[0].text
        dict_product["type"] = product_type
       
    except:
        pass

    try:
        reference = driver.find_elements(By.XPATH,'/html/body/div[5]/div/div[1]/div/div[2]')[0].text
        dict_product["reference"] = reference
    except:
        pass


    keys = driver.find_elements(By.XPATH,"//div[@class='produto-label']")
    values = driver.find_elements(By.XPATH,"//div[@class='produto-info']")
    cont = 0
    for key in keys:
        dict_product[key.text] = values[cont].text
        cont+=1

   
    image = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[1]/div[1]/div[1]/div/img')
    imgcont = 0
    for img in image:
        dict_product["image"+str(cont)] = img.get_attribute("src")
        imgcont +=1
        

    print(dict_product)
    list_product.append(dict_product)

dados = pd.DataFrame(list_product)
dados.to_excel("produtos_incepa.xlsx", index=False)
    

    


    



