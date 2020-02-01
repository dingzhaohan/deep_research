import scrapy
import pandas as pd
import urllib
import json
from spider.items import SpiderItem
#dir = '/Users/zhaohan/Desktop/papers-with-abstracts.json'
dir = '/Users/zhaohan/Desktop/deep_research/data/links-between-papers-and-code.json'
df = pd.read_json(dir)

class BigSpider(scrapy.Spider):
    name = 'big'
    allowed_domains = ['paperswithcode.com', 'github.com', 'arxiv.org', 'semanticscholar.org']
    start_urls = []
    for i in range(len(df)):
        #title = df["paper_title"][i]
        #title = title.replace(' ', '+').replace(':', '%3A').replace(',', '%2C')
        #start_urls.append('https://paperswithcode.com/search?q='+title)
        start_urls.append(df["paper_url"][i])

    def parse(self, response):
        item = SpiderItem()
        position = list(df["paper_url"]).index(response.url)
        item["ppc_arxiv_id"] = df["paper_arxiv_id"][position]
        item["paper_title"] = df["paper_title"][position].strip()
        #print(item["ppc_arxiv_id"])
        abstract = response.xpath('//div[@class="paper-abstract"]/div/div/p/text()').extract_first()
        if abstract:
            try:
                hideabstract = response.xpath('//div[@class="paper-abstract"]/div/div/p/span/text()').extract()[1]
                item["paper_abstract"] = (abstract + hideabstract).replace('\n', '').strip()
            except:
                item["paper_abstract"] = abstract.replace('\n', '').strip()
        else:
            item["paper_abstract"] = None
        item["ppc_all_repo_address"] = response.xpath(
            '//div[@id="id_paper_implementations_collapsed"]/div/div/div/a/@href').extract()
        item["ppc_star"] = []
        star_number = response.xpath(
            '//div[@id="id_paper_implementations_collapsed"]/div/div[@class="col-md-3"]/div/text()').extract()

        index = len(star_number)
        for i in range(1, index, 2):
            item["ppc_star"].append(star_number[i].replace('\n', '').replace(',', '').strip())

        tags = response.xpath('//div[@class="paper-tasks"]/div/div/ul/li/a/@href').extract()

        item["ppc_tasks_classification"] = []
        for tag in tags:
            tag = tag.replace('/task/', '').replace('-', ' ')
            item["ppc_tasks_classification"].append(tag)

        frames = response.xpath(
            '//div[@id="id_paper_implementations_collapsed"]/div/div[@class="col-md-2"]/div/img/@src').extract()
        item["ppc_codeframe"] = []
        if frames:
            for frame in frames:
                frame = frame.replace('/static/frameworks/', '').replace('.png', '').replace('py', '')
                item["ppc_codeframe"].append(frame)

        git_repo_url = item["ppc_all_repo_address"][0].replace('github.com', 'api.github.com/repos') + "?client_id=a26c83afeb1a41304d10&client_secret=ea8586a6b1d16c9f645112fd04b5bf57f5bae88e"
        yield scrapy.Request(git_repo_url, meta={"item": item}, callback=self.parse_git)

    def parse_git(self, response):
        item = response.meta["item"]
        sites = json.loads(response.body_as_unicode())
        #item["repo_size"] = sites["size"]
        #item["repo_url"] = sites["html_url"]
        item["git_watch"] = sites["subscribers_count"]
        item["git_fork"] = sites["forks_count"]
        item["git_star"] = sites["stargazers_count"]
        item["git_repo_created_time"] = sites["created_at"][:10]
        #item["repo_updated_at"] = sites["updated_at"][:10]
        #item["repo_kept_time"] = caltime(item["repo_created_at"], item["repo_updated_at"])
        item["git_open_issues_count"] = int(sites["open_issues_count"])
        item["git_readme_size"] = 0
        url = response.url.replace('?client_id','/issues?client_id')
        yield scrapy.Request(url, meta={"item": item}, callback=self.parse_git_issues)

    def parse_git_issues(self, response):
        sites = json.loads(response.body_as_unicode())
        item = response.meta["item"]
        # try:
        #     item["git_latest_issue_create"] = sites[0]["created_at"][:10]
        # except:
        #     item["git_latest_issue_create"] = None
        try:
            item["git_latest_issue_update_time"] = sites[0]["updated_at"][:10]
        except:
            item["git_latest_issue_update_time"] = None

        #url = response.url.replace('?client_id','/contents/README.md?client_id')
        #print(item["ppc_arxiv_id"])
        if item["ppc_arxiv_id"]:
            url = 'https://api.semanticscholar.org/v1/paper/arXiv:' + str(item["ppc_arxiv_id"])
            #print(url)
            item["ppc_arxiv_address"] = "https://arxiv.org/pdf/" + item["ppc_arxiv_id"]
            yield scrapy.Request(url, meta={"item": item}, callback=self.parse_ssr)
        else:
            print("ssr not exist")
            item["ppc_arxiv_address"] = "Unknown"
            item["paper_author"] = ["Unknown"]
            item["ssr_citation"] = 0
            item["ssr_tasks_classification"] = ["Unknown"]
            item["ssr_venue"] = "Unknown"
            item["ssr_paper_submit_year"] = "Unknown"
            item["ssr_img_address"] = "Unknown"
            item["ssr_img_count"] = 0
            item["ssr_influence"] = 0
            yield item
        

    def parse_git_readme(self, response):
        sites = json.loads(response.body_as_unicode())
        item = response.meta["item"]
        try:
            item["readme_size"] = sites["size"]
        except:
            url = response.url.replace("README", "readme")
            yield scrapy.Request(url, meta={"item":item}, callback=self.detail_parse2)
        return item

    def parse_ssr(self, response):
        json_data = json.loads(response.body_as_unicode())
        item = response.meta["item"]
        item["paper_author"] = []
        for i in json_data["authors"]:
            item["paper_author"].append(i["name"])
        #item["citationVelocity"] = json_data["citationVelocity"]
        item["ssr_citation"] = len(json_data["citations"])
        #item["doi"] = json_data["doi"]
        #item["influentialCitationCount"] = json_data["influentialCitationCount"]
        #item["references"] = json_data["references"]
        #item["title"] = json_data["title"]
        item["ssr_tasks_classification"] = []
        for i in json_data["topics"]:
            item["ssr_tasks_classification"].append(i['topic'])
        #item["url"] = json_data["url"]
        item["ssr_venue"] = json_data["venue"]
        item["ssr_paper_submit_year"] = json_data["year"]
        #print(item)
        item["ssr_img_address"] = ""
        item["ssr_img_count"] = 0
        item["ssr_influence"] = json_data["influentialCitationCount"]

        #url = 'https://www.semanticscholar.org/search?q=' + item['paper_title'].replace(' ', '%20').replace("'", "%27").replace(':', '%3A').replace('(', '%28').replace(')', '%29')
        #yield scrapy.Request(url, meta={"item": item}, callback=self.parse_ssr_img)
        return item

    def parse_ssr_img(self, response):
        img_src = response.xpath('//ul[@class="flex-row paper-detail-figures-list"]/li/a/@href').extract()
        item["img_src"] = []
        for i in img_src:
            item["img_src"].append("https://www.semanticscholar.org" + i)
        item["img_num"] = len(item["img_src"])
        yield item
