# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# pipelines.py
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import csv


class UnsplashPipeline:
    def process_item(self, item, spider):
        return item


class UnsplashImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_url'])

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if image_path:
            item['local_path'] = image_path[0]
        return item


class CSVExportPipeline:
    def __init__(self):
        self.file = open('images_info.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=['image_url', 'image_title', 'category', 'local_path'])
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()
