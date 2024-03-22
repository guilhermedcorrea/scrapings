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


list_categories = ["https://www.br.roca.com/produtos/cubas-lavatorios",
                   "https://www.br.roca.com/produtos/moveis",
                   "https://www.br.roca.com/produtos/sistemas-instalacao",
                   "https://www.br.roca.com/produtos/mictorios",
                   "https://www.br.roca.com/produtos/acessorios",
                   "https://www.br.roca.com/produtos/metais-sanitarios",
                   "https://www.br.roca.com/produtos/chuveiros",
                   "https://www.br.roca.com/produtos/smart-toilets",
                   "https://www.br.roca.com/produtos/bacias-sanitarias",
                   "https://br.roca.com/produtos/pias-cubas-cozinha",
                   "https://www.br.roca.com/produtos/assentos-tampas-sanitarias",
                   "https://www.br.roca.com/produtos/espelhos",
                   "https://www.br.roca.com/produtos/banheiras",
                   "https://www.br.roca.com/produtos/bides",
                   "https://www.br.roca.com/produtos/lavatorios-suspensos",
                   "https://www.br.roca.com/produtos/cubas-apoio",
                   "https://www.br.roca.com/produtos/cubas-sobrepor",
                   "https://www.br.roca.com/produtos/cubas-embutir",
                   "https://www.br.roca.com/produtos/lavatorios-coluna"]



url_list = []


for categories in list_categories:
    try:
        driver.get(categories)
    except:
        pass


    time.sleep(3)
    try:
        products = driver.find_elements(By.XPATH,"//div[@class='wrapper-producto']//a")
        for product in products:
          
            url = product.get_attribute("href")
            if url not in url_list:
                url_list.append(url)
    except:
        pass


list_products = []

url_list = list(set(url_list))
for url in url_list:
    dict_products = {}
    try:
        driver.get(url)
        time.sleep(1)
        print(url)
    except:
        pass

#driver.get("https://www.br.roca.com/produtos/dispenser-sabonete-liquido-817673..0?sku=A817673C60")
    try:
        name = driver.find_elements(By.XPATH,'//*[@id="prod-name"]')[0].text
        dict_products["name"] = name
    except:
        print("erro name")
        
    
    try:
        cod = driver.find_elements(By.XPATH,'//*[@id="prod-ref"]')[0].text
        dict_products["reference"] = cod.split(":")[-1].strip()
    except:
        pass


    try:
        ref1 = driver.find_elements(By.XPATH,'//*[@id="anclaProductDetail"]/div[2]/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div/label')[0].text
        
    except:
        pass

    try:
        val1 = driver.find_elements(By.XPATH,'//*[@id="dim-txt"]')[0].text
        
        dict_products[ref1.strip().split(":")[0].lower()] = val1
    except:
        pass



    
    try:
        images = driver.find_elements(By.XPATH,'//*[@id="anclaProductDetail"]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div/div/div/a/img')
        cont = 0
        for image in images:
            dict_products["image"+str(cont)] = image.get_attribute("src")
            cont+=1
            #print(image.get_attribute("src"))
    except:
        pass


    try:
        refs = driver.find_elements(By.XPATH,"//div[@class='row r-body ']//p")
        for ref in refs:
            key = ref.text.strip().split(":")[0]
            value = ref.text.strip().split(":")[-1]
            dict_products[key] = value
            
    except:
        pass

    
    print(dict_products)

    list_products.append(dict_products)
    

dados = pd.DataFrame(list_products)
dados.to_excel("produtos_rocca.xlsx", index=False)

