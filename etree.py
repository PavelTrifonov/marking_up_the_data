import requests
from lxml import html
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0\
            YaBrowser/24.1.0.0 Safari/537.36'}
resp = requests.get(url="https://www.imdb.com/chart/top/?ref_=nv_mv_250",
                    headers=headers)
# resp.encoding = 'utf-8'

tree = html.fromstring(html=resp.content)
movies = tree.xpath("//ul[@role='presentation']/li/div[@class='ipc-metadata-list-summary-item__c']/div/div")
movies_list = []
for movie in movies:
    try:
        age = movie.xpath("./div[@class='sc-be6f1408-7 iUtHEN cli-title-metadata']/span[3]/text()")[0]
    except:
        age = None
    m = {
        'movie': movie.xpath('./div/a/h3/text()')[0],
        'year of issue': movie.xpath("./div[@class='sc-be6f1408-7 iUtHEN cli-title-metadata']/span[1]/text()")[0],
        'duration': movie.xpath("./div[@class='sc-be6f1408-7 iUtHEN cli-title-metadata']/span[2]/text()"),
        'age': age,
        'rating': movie.xpath('./span/div/span/text()')[0]
    }
    movies_list.append(m)

pprint(movies_list)
print(len(movies_list))
# body = tree.find("body/p")
# li = tree.findall('body/ul/li')
# # print(li[0].text, li[1].text)
# teg_p = tree.xpath('//p/text()')[0]
# print(teg_p)
# # print(teg_p[0].text)
# # 
# # print(body.text)