# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os


class JobFromHhPipeline:
    def data_cleaning(self, item):
        salary = "".join(item['salary']).replace("\xa0", '').replace("от ", "").replace(" до ", "-")
        item['salary'] = salary
        organization = "".join(set(item['organization']))
        address = "".join(set(item['address']))
        experience = "".join(item['experience'])
        item['organization'] = organization
        item['address'] = address
        item['experience'] = experience

    def write_to_csv(self, data, filename):
        # Проверяем, существует ли файл
        file_exists = os.path.isfile(filename)
        # Открываем файл в режиме добавления (a) или создаем новый файл для записи
        with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            # Если файл только что создан, записываем заголовки
            if not file_exists:
                writer.writeheader()
            # Записываем данные в файл
            writer.writerow(data)

    def process_item(self, item, spider):
        # Преобразуем объект item в словарь, чтобы передать его в функцию write_to_csv
        data = ItemAdapter(item).asdict()
        self.data_cleaning(data)
        self.write_to_csv(data, f"{spider.name}.csv")
        return item
