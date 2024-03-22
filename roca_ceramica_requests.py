import requests
from bs4 import BeautifulSoup
import pandas as pd


dados = pd.read_excel(r"D:\scrapings_portobello\urls_roca_ceramica.xlsx")
urls = dados.to_dict(orient='records')

list_products = []

for url_data in urls:
    print(url_data["url"])

  
    response = requests.get(url_data["url"])
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')

       
        dict_product = {}

        
        name = soup.find('h2').text.strip()
        dict_product["name"] = name

       
        product_type_elem = soup.find('div', class_='descricao-curta')
        if product_type_elem:
            product_type = product_type_elem.text.strip()
            dict_product["type"] = product_type

        
        reference_elem = soup.find('div', class_='codigo_produto align-self-center')
        if reference_elem:
            reference = reference_elem.text.strip().split(":")[-1].strip()
            dict_product["reference"] = reference

       
        line_elem = soup.find('h1', class_='titulo')
        if line_elem:
            line = line_elem.text.strip()
            dict_product["line"] = line

       
        images = soup.find_all('img', class_='img-fluid')
        image_urls = []
        for image in images:
            image_url = image['src']
            image_urls.append(image_url)
        dict_product['images'] = ', '.join(image_urls)

        
        specifications = soup.find_all('div', class_='col-sm-6')
        labels = soup.find_all('div', class_='produto-label')
        values = soup.find_all('div', class_='produto-info')
        
        for label, value in zip(labels, values):
            key = label.text.strip()
            value = value.text.strip()
            dict_product[key] = value

       
        list_products.append(dict_product)

      
        print(dict_product)

    else:
        print(f"Erro ao acessar o URL {url_data['url']}")
