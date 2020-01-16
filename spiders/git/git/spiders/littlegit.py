# -*- coding: utf-8 -*-
import scrapy


class LittlegitSpider(scrapy.Spider):
    name = 'littlegit'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/']

    def parse(self, response):
        pass
