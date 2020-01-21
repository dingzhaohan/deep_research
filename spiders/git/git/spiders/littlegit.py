# -*- coding: utf-8 -*-
import scrapy
from git.items import GitItem
import pandas as pd
import json
import time
import datetime
# df = pd.read_json("/home/zhaohan/Desktop/research/lastdata_papers_with_code_repo.json")
df = pd.read_json('/Users/zhaohan/Desktop/deep_research/data/links-between-papers-and-code.json')
'''
repo = set()
for i in range(len(df)):
    for url in df["repo_url"][i]:
        repo.add(url)
'''
class LittlegitSpider(scrapy.Spider):
    name = 'littlegit'
    allowed_domains = ['github.com']
    start_urls = []
    '''
    for i in repo:
        url = "https://api.github.com/repos" + i[18:] + "?client_id=a26c83afeb1a41304d10&client_secret=ea8586a6b1d16c9f645112fd04b5bf57f5bae88e"
        start_urls.append(url)
    '''
    for i in range(len(df)):
        url = "https://api.github.com/repos" + df["repo_url"][i][18:] + "?client_id=a26c83afeb1a41304d10&client_secret=ea8586a6b1d16c9f645112fd04b5bf57f5bae88e"
        start_urls.append(url)

    def parse(self, response):

        index = self.start_urls.index(response.url)

        item = GitItem()

        sites = json.loads(response.body_as_unicode())

        item["paper_title"] = df["paper_title"][index]

        item["repo_size"] = sites["size"]

        # item["repo_name"] = sites["name"]

        item["repo_url"] = sites["html_url"]

        item["git_watch"] = sites["subscribers_count"]

        item["git_fork"] = sites["forks_count"]

        item["git_star"] = sites["stargazers_count"]

        item["repo_created_at"] = sites["created_at"][:10]

        item["repo_updated_at"] = sites["updated_at"][:10]

        item["repo_kept_time"] = caltime(item["repo_created_at"], item["repo_updated_at"])

        item["open_issues_count"] = sites["open_issues_count"]

        url1 = response.url.replace('?client_id=a26c83afeb1a41304d10&client_secret=ea8586a6b1d16c9f645112fd04b5bf57f5bae88e','/issues?client_id=a26c83afeb1a41304d10&client_secret=ea8586a6b1d16c9f645112fd04b5bf57f5bae88e')

        #yield scrapy.Request(url1, meta={"item":item}, callback=self.detail_parse1)

        yield item

    def detail_parse1(self, response):
        sites = json.loads(response.body_as_unicode())
        item = response.meta["item"]
        try:
            item["latest_issues_created_at"] = sites[0]["created_at"][:10]
        except:
            item["latest_issues_created_at"] = None
        try:
            item["latest_issues_updated_at"] = sites[0]["updated_at"][:10]
        except:
            item["latest_issues_updated_at"] = None
        print(response.url)
        #url2 = response.url.replace('?client_id=a26c83afeb1a41304d10&client_secret=ea8586a6b1d16c9f645112fd04b5bf57f5bae88e','/contents/README.md?client_id=a26c83afeb1a41304d10&client_secret=ea8586a6b1d16c9f645112fd04b5bf57f5bae88e')
        #yield scrapy.Request(url2, meta={"item": item}, callback=self.detail_parse2)


    def detail_parse2(self, response):
        sites = json.loads(response.body_as_unicode())
        item = response.meta["item"]
        try:
            item["readme_size"] = sites["size"]
        except:
            url = response.url.replace("README", "readme")
            yield scrapy.Request(url, meta={"item":response.meta["item"]}, callback=self.detail_parse2)
        return item

def caltime(date1, date2):
    date1 = time.strptime(date1, "%Y-%m-%d")
    date2 = time.strptime(date2, "%Y-%m-%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    return str((date2 - date1)).replace(" days, 0:00:00", "")

