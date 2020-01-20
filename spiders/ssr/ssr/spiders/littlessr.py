# -*- coding: utf-8 -*-

import pandas as pd
import scrapy
import json
df = pd.read_json('/Users/zhaohan/Desktop/Grade3/本研/json_data/papers_with_abstracts.json')

class LittlessrSpider(scrapy.Spider):
    name = 'littlessr'
    allowed_domains = ['arxiv.org']
    start_urls = []

    for i in range(len(df)):
        if df["arxiv_id"][i]:
            start_urls.append('https://api.semanticscholar.org/v1/paper/arXiv:' + str(df["arxiv_id"][i]))

    def parse(self, response):
        item = SementicItem()
        json_data = json.loads(response.body_as_unicode())
        item["abstract"] = json_data["abstract"]
        item["arxivId"] = json_data["arxivId"]
        item["authors"] = json_data["authors"]
        item["citationVelocity"] = json_data["citationVelocity"]
        item["citations"] = json_data["citations"]
        item["doi"] = json_data["doi"]
        item["influentialCitationCount"] = json_data["influentialCitationCount"]
        item["references"] = json_data["references"]
        item["title"] = json_data["title"]
        item["topics"] = json_data["topics"]
        item["url"] = json_data["url"]
        item["venue"] = json_data["venue"]
        item["year"] = json_data["year"]
        yield item