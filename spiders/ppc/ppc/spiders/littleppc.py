# -*- coding: utf-8 -*-
import scrapy


class LittleppcSpider(scrapy.Spider):
    name = 'littleppc'
    allowed_domains = ['papwerswithcode.com']
    start_urls = ['http://papwerswithcode.com/']

    def parse(self, response):
        pass
