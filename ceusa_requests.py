import requests
from bs4 import BeautifulSoup

max_page = 2
urls = []

for page in range(1, max_page + 1):
    url = f"https://www.ceusa.com.br/pt/produtos?_page={page}&query=&formato=&cores="
    response = requests.get(url)
    if response.status_code == 200:  
        soup = BeautifulSoup(response.content, 'html.parser')
        product_links = soup.find_all('a', class_='absolute')  
        for link in product_links:
            href = link.get('href')
            if href and "/pt/produtos/" in href:  
                product_url = f"https://www.ceusa.com.br{href}"  
                print(product_url)
                print(page)
                urls.append(product_url)
    else:
        print(f"Erro ao acessar a página {page}")

list_products = []

for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        dict_product = {}

        try:
            name = soup.select_one('span.text-white.uppercase').text.strip()
            print(name)
            dict_product["name"] = name
        except Exception as e:
            print(f"Erro ao obter o nome do produto: {e}")

'''
        try:
            image = soup.select_one('img.product-image')
            src_value = image['src']
            dict_product["image"] = src_value
        except Exception as e:
            print(f"Erro ao obter a imagem do produto: {e}")

        spaces = soup.select('div.product-specs p')
        num_p_elements = len(spaces)

        for i in range(num_p_elements):
            if num_p_elements - i >= 2:
                key = spaces[i].text.strip()
                values = [p.text.strip() for p in spaces[i+1:]]
                dict_product[key] = values

        referencias = soup.select('div.product-references table tbody tr')
        data_dict = {}

        for ref in referencias:
            tds = ref.find_all('td')
            if len(tds) >= 2:
                key = tds[0].text.strip()
                value = tds[1].text.strip()
                data_dict[key] = value

        dict_product.update(data_dict)

        print(dict_product)
        list_products.append(dict_product)
    else:
        print(f"Erro ao acessar o URL {url}")
'''