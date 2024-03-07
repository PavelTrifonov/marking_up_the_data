# from pars_unsplash.items import ImageItem
import scrapy
from scrapy.http import HtmlResponse
from pars_unsplash.items import ParsUnsplashItem


class ImagesParsSpider(scrapy.Spider):
    name = "images_pars"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response: HtmlResponse):
        # Получаем ссылки на категории фотографий
        categories = response.xpath('//a[contains(@class, "p7ajO KHq0c")]/@href').getall()
        for category in categories:
            yield response.follow(category, callback=self.parse_category)

    def parse_category(self, response: HtmlResponse):
        # Получаем ссылки на страницы с изображениями в выбранной категории
        image_pages = response.xpath('//a[@itemprop="contentUrl"]/@href').getall()
        for image_page in image_pages:
            yield response.follow(image_page, callback=self.parse_image)

    def parse_image(self, response: HtmlResponse):
        # Извлекаем данные о изображении
        image = ParsUnsplashItem()
        image['image_url'] = response.xpath('//div[@class="MorZF"]/img/@src').get()
        image['image_title'] = response.xpath('//h1[@class="la4U2"]/text()').get()
        image['category'] = response.xpath('//title/text()').get()
        image['local_path'] = ''  # Путь будет добавлен после загрузки
        yield image




    # def parse(self, response: HtmlResponse):
    #     categories = response.xpath('.//div[@class="pRk2s"]//a[contains(@class, "p7ajO")]/@href').getall()
    #     for category in categories[3]:
    #         if category:
    #             # name_category = response.xpath("//h1[@class='xKyJX sjMaL']//text()").get()
    #             yield response.follow(category, callback=self.category_images_parse)

    # def category_images_parse(self, response: HtmlResponse):
    #     images = response.xpath('//div[@class="MorZF"]//@srcset').getall()
    #     for image in images:
    #         yield response.follow(image, callback=self.image_parse)

    # def image_parse(self, response: HtmlResponse):
    #     # name_category = response.xpath("//h1[@class='xKyJX sjMaL']//text()").get()
    #     url = response.url
    #     image = response.xpath("//img[@class='_2zEKz']/@src").get()
    #     yield ParsUnsplashItem(image=image, url=url)
