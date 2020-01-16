# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 论文标题
    paper_title = scrapy.Field()

    # 论文摘要
    paper_abstract = scrapy.Field()

    # 论文地址
    paper_url_abs = scrapy.Field()

    # 论文下载地址
    paper_url_pdf = scrapy.Field()

    # github代码地址
    repo_url = scrapy.Field()

    # 论文被标记的次数
    star_number = scrapy.Field()

    # 论文采用哪种框架，如tensorflow或者pytorch
    frame = scrapy.Field()

    # 论文所解决的任务，如computer vision，nlp等
    task = scrapy.Field()


