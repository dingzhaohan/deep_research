# -*- coding: utf-8 -*-
import scrapy


class LittlessrSpider(scrapy.Spider):
    name = 'littlessr'
    allowed_domains = ['semantic.scholar.com']
    start_urls = ['http://semantic.scholar.com/']

    def parse(self, response):
        pass
