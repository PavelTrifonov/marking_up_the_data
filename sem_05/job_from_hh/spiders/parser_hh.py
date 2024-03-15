import scrapy
from scrapy.http import HtmlResponse
from job_from_hh.items import JobFromHhItem


class ParserHhSpider(scrapy.Spider):
    name = "parser_hh"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://samara.hh.ru/search/vacancy?text=Аналитик+данных&from=suggest_post&area=78&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"]

    def parse(self, response: HtmlResponse):
        links = response.xpath('//span/a[@class="bloko-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[@data-qa='pager-page']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//span/a[@class="bloko-link"]/span/text()').get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']/span/text()").getall()
        organization = response.xpath("//span[@data-qa='bloko-header-2']//text()").getall()
        address = response.xpath("//a/span[@data-qa='vacancy-view-raw-address']//text()").getall()
        experience = response.xpath("//span[@data-qa='vacancy-experience']//text()").getall()
        url = response.url
        yield JobFromHhItem(name=name, salary=salary, url=url,
                            organization=organization, address=address,
                            experience=experience)
