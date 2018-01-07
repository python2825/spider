# -*- coding: utf-8 -*-
from movieproject.items import MovieprojectItem
import scrapy



class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/index.html/']
    def parse(self, response):
        table_list = response.xpath('div[@class="co_content"]/ul/table')
        for table in table_list:
            item = MovieprojectItem()

            item['name'] = table.xpath('.//a[@class="ulink"]/text()').extract_first()
            item['movie_info'] = table.xpath('.//tr[last()]/td/text()').extract_first()
            movie_url = 'http://www.dytt8.net' + table.xpath('.//a[@class="ulink"]/@href').extract_first()
            yield scrapy.Request(url=movie_url, callback=self.parse_info, meta={'item': item})

    def parse_info(self, response):
        item = response.meta['item']
        item['image_url'] = response.xpath('//div[@id="Zoom"]//img[1]/@src').extract_first()
        item['download_url'] = response.xpath('//td[@bgcolor="#fdfddf"]/a/text()').extract_first()
        yield item