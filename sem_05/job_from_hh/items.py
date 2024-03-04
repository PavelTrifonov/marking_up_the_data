# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobFromHhItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    organization = scrapy.Field()
    address = scrapy.Field()
    experience = scrapy.Field()
