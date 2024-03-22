from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)




driver.get("https://www.decortiles.com/produtos")

time.sleep(90)


lista_urls = []


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


scroll_to_bottom(driver)


urls = driver.find_elements(By.XPATH, '//*[@id="ulProdutosHome"]/li//a')


for url in urls:
    lista_urls.append(url.get_attribute("href"))


dados = pd.DataFrame({'urls': lista_urls})


dados.to_excel("urls_decorstile.xlsx", index=False)

