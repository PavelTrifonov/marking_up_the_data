import requests # для запросов к сайту
from lxml import html # для парсинга html
from pprint import pprint # для вывода в консоль js в читабельном формате
from fake_useragent import UserAgent # для генерации User-Agent
import pandas as pd # для создания датафрейма
from urllib.parse import urlencode # для формирования URL
import logging # для логирования ошибок

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Указываем стартовую страницу
page = 0
# Формируем словарь, который будем наполнять
job_dict = {'name': [],
            'salary': [],
            'currency': [],
            'organization': [],
            'city': [],
            'experience': [],
            'link': []
            }
# Задаем название специальности для поиска
job_title = input("Какую вакансию ищем?  ")
# Запускаем цикл по парсингу всех интересующих страниц
while True:
    base_url = "https://samara.hh.ru/search/vacancy"
    # Параметры запроса
    params = {
        'area': '78',
        'search_field': ['name', 'description'],
        'enable_snippets': 'false',
        'disableBrowserCache': 'true',
        'hhtmFrom': 'vacancy_search_list',
        'label': 'not_from_agency',
        'text': job_title,
        'page': page
    }
    # Составляем полный URL
    full_url = base_url + '?' + urlencode(params)
    print(full_url)
    # Отправляем запрос к сайту HH
    resp = requests.get(url=full_url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"})
    # Создаем дерево элементов HTML из контента, полученного в ответ на запрос
    tree = html.fromstring(html=resp.content)
    # Ищем интересующую нас информация в HTML-документе
    jobsvacancies = tree.xpath('//div[@class="vacancy-serp-item__layout"]')
    if jobsvacancies:  # если возвращает пустой список, завершаем цикл обработки сайта
        print(f"Обрабатывается {page} страница")
        for job in jobsvacancies:
            try:
                job_dict["name"].append(job.xpath('.//h3/span/span/a/span/text()')[0])
            except Exception as e:
                logging.error("Ошибка в блоке 1: %s", e)
                job_dict["name"].append(None)
            try:
                salary_text = job.xpath('.//span[@data-qa="vacancy-serp__vacancy-compensation"]/text()')
                salary = "".join(salary_text[:-1]).strip().replace("\u202f", "")
                job_dict["currency"].append(salary_text[-1])
                job_dict["salary"].append(salary)
            except Exception as e:
                logging.error("Ошибка в блоке 2: %s", e)
                job_dict["salary"].append(None)
                job_dict["currency"].append(None)
            try:
                job_dict["organization"].append("".join(job.xpath('.//a[@data-qa="vacancy-serp__vacancy-employer"]/text()')).replace("\xa0"," "))
            except Exception as e:
                logging.error("Ошибка в блоке 3: %s", e)
                job_dict["organization"].append(None)
            try:
                job_dict['city'].append(job.xpath('//div[@data-qa="vacancy-serp__vacancy-address"]/text()')[0])
            except Exception as e:
                logging.error("Ошибка в блоке 4: %s", e)
                job_dict['city'].append(None)
            try:
                experience = job.xpath('.//div[@data-qa="vacancy-serp__vacancy-work-experience"]/text()')
                job_dict['experience'].append(experience[0] if experience else None)
            except Exception as e:
                logging.error("Ошибка в блоке 5: %s", e)
                job_dict['experience'].append(None)
            try:
                job_dict['link'].append(job.xpath('.//a[@class="bloko-link"]/@href')[0])
            except Exception as e:
                logging.error("Ошибка в блоке 6: %s", e)
                job_dict['link'].append(None)
    else:
        break
    page += 1

# создаем дата фрейм на основе полученных данных и записываем его в csv
df = pd.DataFrame(job_dict)
df.to_csv(f"{job_title}.csv", index=False)
print(df)
