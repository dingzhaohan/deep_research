# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    repo_size = scrapy.Field()

    repo_name = scrapy.Field()

    repo_url = scrapy.Field()

    repo_created_at = scrapy.Field()

    repo_updated_at = scrapy.Field()

    git_watch = scrapy.Field()

    git_fork = scrapy.Field()

    git_star = scrapy.Field()

    latest_issues_created_at = scrapy.Field()

    latest_issues_updated_at = scrapy.Field()

    open_issues_count = scrapy.Field()

    readme_size = scrapy.Field()

    repo_kept_time = scrapy.Field()

    paper_title = scrapy.Field()