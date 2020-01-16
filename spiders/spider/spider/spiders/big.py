import scrapy
import pandas as pd
import urllib
from spider.items import SpiderItem
#dir = '/Users/zhaohan/Desktop/papers-with-abstracts.json'
dir = '/Users/zhaohan/Desktop/deep_research/data/links-between-papers-and-code.json'
df = pd.read_json(dir)

class BigSpider(scrapy.Spider):
    name = 'big'
    allowed_domains = ['paperswithcode.com']
    start_urls = []
    for i in range(len(df)):
        title = df["paper_title"][i]
        if title == None:
            continue
        title = title.replace(' ', '+').replace(':', '%3A').replace(',', '%2C')
        start_urls.append('https://paperswithcode.com/search?q='+title)

    def parse(self, response):
        for link in response.xpath('//h1/a/@href').extract():
            yield scrapy.Request(response.urljoin(link), callback=self.parse1)


    def parse1(self, response):
        item = SpiderItem()
        item["paper_title"] = response.xpath('//div[@class="paper-title"]/div/div/h1/text()').extract_first()
        abstract = response.xpath('//div[@class="paper-abstract"]/div/div/p/text()').extract_first()
        try:
            hideabstract = response.xpath('//div[@class="paper-abstract"]/div/div/p/span/text()').extract()[1]
            item["paper_abstract"] = (abstract + hideabstract).replace('\n', '')
        except:
            item["paper_abstract"] = abstract.replace('\n', '')
        item["repo_url"] = response.xpath(
            '//div[@id="id_paper_implementations_collapsed"]/div/div/div/a/@href').extract()
        item["star_number"] = []
        star_number = response.xpath(
            '//div[@id="id_paper_implementations_collapsed"]/div/div[@class="col-md-3"]/div/text()').extract()

        index = len(star_number)
        for i in range(1, index, 2):
            item["star_number"].append(star_number[i].replace('\n', '').replace(',', '').strip())

        tags = response.xpath('//div[@class="paper-tasks"]/div/div/ul/li/a/@href').extract()

        item["task"] = []
        for tag in tags:
            tag = tag.replace('/task/', '').replace('-', ' ')
            item["task"].append(tag)

        item["paper_url_pdf"] = response.xpath('//div[@class="paper-abstract"]/div/div/a/@href').extract()[0]
        item["paper_url_abs"] = response.xpath('//div[@class="paper-abstract"]/div/div/a/@href').extract()[1]
        frames = response.xpath(
            '//div[@id="id_paper_implementations_collapsed"]/div/div[@class="col-md-2"]/div/img/@src').extract()
        item["frame"] = []
        if frames:
            for frame in frames:
                frame = frame.replace('/static/frameworks/', '').replace('.png', '').replace('py', '')
                item["frame"].append(frame)
        return item