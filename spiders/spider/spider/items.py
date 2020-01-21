# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    paper_title = scrapy.Field()
    paper_author = scrapy.Field()
    paper_abstract = scrapy.Field()
    git_star = scrapy.Field()
    git_watch = scrapy.Field()
    git_fork = scrapy.Field()
    git_readme_size = scrapy.Field()
    git_open_issues_count = scrapy.Field()
    git_latest_issue_update_time = scrapy.Field()
    git_repo_created_time = scrapy.Field()
    ppc_star = scrapy.Field()
    ppc_codeframe = scrapy.Field()
    ppc_tasks_classification = scrapy.Field()
    ppc_all_repo_address = scrapy.Field()
    ppc_arxiv_address = scrapy.Field()
    ppc_arxiv_id = scrapy.Field()
    ssr_citation = scrapy.Field()
    ssr_tasks_classification = scrapy.Field()
    ssr_img_address = scrapy.Field()
    ssr_img_count = scrapy.Field()
    ssr_influence = scrapy.Field()
    ssr_venue = scrapy.Field()
    ssr_paper_submit_year = scrapy.Field()
    #model_input = scrapy.Field()
    #model_output = scrapy.Field()
    #datasets = scrapy.Field()
    #datasets_public = scrapy.Field()
    #model_reach_sota = scrapy.Field()
    #optimize_method = scrapy.Field()
    #docker_image = scrapy.Field()
    #code_language = scrapy.Field()
    #code_version = scrapy.Field()
    #pretrained_model = scrapy.Field()
    #network_arch = scrapy.Field()

