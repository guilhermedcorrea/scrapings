from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver = webdriver.Chrome(options=options)


max_page = 2


urls = []


for page in range(1, max_page + 1):
   
    url = f"https://www.ceusa.com.br/pt/produtos?_page={page}&query=&formato=&cores="
    driver.get(url)

  

    driver.implicitly_wait(3)

   
    try:
        divs = driver.find_elements(By.XPATH,'/html/body/form/div/div[2]/div[2]/div/div/div/div/div/a')
        for div in divs:
            print(div.get_attribute("href"))
            print(page)
            urls.append(div.get_attribute("href"))
    except:
        pass


list_products = []
for url in urls:
    driver.get(url)

    time.sleep(3)

    dict_product = {}

    try:
        name = driver.find_elements(By.XPATH,'/html/body/main/div[1]/div[1]/span[3]')[0].text
        print(name)
        dict_product["name"] = name
    except:
        pass


    try:
        wait = WebDriverWait(driver, 2)
        imagem_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[1]/img')))

    
        src_value = imagem_element.get_attribute('src')
        dict_product["image"] = src_value
    except:
        pass



    spaces = driver.find_elements(By.XPATH, '//*[@id="box-detalhe"]/div[1]/div[1]/div[1]/div/div/div/div//p')

    num_p_elements = len(spaces)

    for i in range(num_p_elements):
      
        if num_p_elements - i >= 2:
           
            chave = spaces[i].text

          
            valores = [p.text for p in spaces[i+1:]]

          
            data_dict = {chave: valores}

           
            dict_product.update(data_dict)
       
      
    referencias = driver.find_elements(By.XPATH, '//*[@id="box-detalhe"]/div[1]/div[2]/div/table/tbody/tr')

    data_dict = {}

    for ref in referencias:
        
        tds = ref.find_elements(By.TAG_NAME, 'td')

       
        if len(tds) >= 2:
            
            chave = tds[0].text
            valor = tds[1].text

           
            data_dict[chave] = valor

    dict_product.update(data_dict)

    print(dict_product)
    list_products.append(dict_product)


dados = pd.DataFrame(list_products)
dados.to_excel("produtos_ceusa.xlsx", index=False)