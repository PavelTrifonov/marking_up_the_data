# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParsUnsplashItem(scrapy.Item):
    image_url = scrapy.Field()
    image_title = scrapy.Field()
    category = scrapy.Field()
    local_path = scrapy.Field()
