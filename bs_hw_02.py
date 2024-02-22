import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
# from pprint import pprint

ua = UserAgent()
headers = {'UserAgent': ua.random}
page = 1
url_0 = 'http://books.toscrape.com'
params = {}
titles = []
rating_dict = {'One': 1, 'Two': 2, 'Three': 3,
               'Four': 4, 'Five': 5}
rating = []
links = []
prices = []
currency = []
presence = []
while True:
    url = f'{url_0}/catalogue/page-{page}.html'
    response = requests.get(url=url)
    if response:
        soup = BeautifulSoup(response.content, "html.parser")
        # pprint(soup.find("article", {'class': 'product_pod'}))
        for row in soup.find_all("article", {'class': 'product_pod'}):
            try:
                titles.append(row.find('img').get('alt'))
            except:
                titles.append(None)
                print('Нет данных о названии')
            try:
                rating.append(rating_dict[row.find('p').get('class')[1]])
            except:
                rating.append(None)
                print('Нет данных о рейтинге')
            try:
                links.append(url_0 + row.find('a').get('href'))
            except:
                links.append(None)
                print('Нет данных о ссылке')
            try:
                price = row.find('p', {'class': 'price_color'}).text
                prices.append(float(price[1:]))
                currency.append(price[0])
            except:
                prices.append(None)
                print('Нет данных о цене')
            try:
                presence.append(row.find('p', {'class': 'instock availability'}).text.strip())
            except:
                presence.append(None)
                print('Нет данных о наличии')
    else:
        break
    print(response.status_code)
    print(f"Идет обработка {page} страницы")
    page += 1
library = pd.DataFrame({'titles': titles, 'rating': rating, 'links': links,
                        'prices': prices, 'currency': currency,
                        'presence': presence})
library.to_json("library.json")
print(library)
