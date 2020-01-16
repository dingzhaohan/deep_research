# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
df = pd.read_json('/home/zhaohan/Desktop/research/links-between-papers-and-code.json')

class BigSpider(scrapy.Spider):
    name = 'big'
    allowed_domains = ['github.com', 'paperswithcode.com']
    start_urls = []

    def parse(self, response):
        pass
