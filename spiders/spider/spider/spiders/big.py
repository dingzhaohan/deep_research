import scrapy
import pandas as pd
import urllib
from spider.items import SpiderItem
#dir = '/Users/zhaohan/Desktop/papers-with-abstracts.json'
dir = '/home/zhaohan/Desktop/deep_research/data/links-between-papers-and-code.json'
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
            yield scrapy.Request(response.urljoin(link), callback=self.parse_ppc)


    def parse_ppc(self, response):
        item = SpiderItem()
        item["paper_title"] = response.xpath('//div[@class="paper-title"]/div/div/h1/text()').extract_first()
        abstract = response.xpath('//div[@class="paper-abstract"]/div/div/p/text()').extract_first()
        try:
            hideabstract = response.xpath('//div[@class="paper-abstract"]/div/div/p/span/text()').extract()[1]
            item["paper_abstract"] = (abstract + hideabstract).replace('\n', '')
        except:
            item["paper_abstract"] = abstract.replace('\n', '')
        item["ppc_all_repo_address"] = response.xpath(
            '//div[@id="id_paper_implementations_collapsed"]/div/div/div/a/@href').extract()
        item["ppc_star"] = []
        star_number = response.xpath(
            '//div[@id="id_paper_implementations_collapsed"]/div/div[@class="col-md-3"]/div/text()').extract()

        index = len(star_number)
        for i in range(1, index, 2):
            item["star_number"].append(star_number[i].replace('\n', '').replace(',', '').strip())

        tags = response.xpath('//div[@class="paper-tasks"]/div/div/ul/li/a/@href').extract()

        item["ppc_tasks_classification"] = []
        for tag in tags:
            tag = tag.replace('/task/', '').replace('-', ' ')
            item["ppc_tasks_classification"].append(tag)

        #item["paper_url_pdf"] = response.xpath('//div[@class="paper-abstract"]/div/div/a/@href').extract()[0]
        item["ppc_arxiv_address"] = response.xpath('//div[@class="paper-abstract"]/div/div/a/@href').extract()[1]
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

        sites = json.loads(response.body_as_unicode())

        #item["repo_size"] = sites["size"]

        #item["repo_url"] = sites["html_url"]

        item["git_watch"] = sites["subscribers_count"]

        item["git_fork"] = sites["forks_count"]

        item["git_star"] = sites["stargazers_count"]

        item["git_repo_created_time"] = sites["created_at"][:10]

        #item["repo_updated_at"] = sites["updated_at"][:10]

        #item["repo_kept_time"] = caltime(item["repo_created_at"], item["repo_updated_at"])

        item["git_open_issues_count"] = sites["open_issues_count"]

        url1 = response.url.replace('?client_id','/issues?client_id')

        yield scrapy.Request(url1, meta={"item":item}, callback=self.parse_git_issues)

    def parse_git_issues(self, response):
        
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

        url = response.url.replace('?client_id','/contents/README.md?client_id')
        yield scrapy.Request()
        

    def parse_git_readme(self, response):
        sites = json.loads(response.body_as_unicode())
        item = response.meta["item"]
        try:
            item["readme_size"] = sites["size"]
        except:
            url = response.url.replace("README", "readme")
            yield scrapy.Request(url, meta={"item":response.meta["item"]}, callback=self.detail_parse2)
        return item

    def parse_ssr(self, response):

        item = SementicItem()

        json_data = json.loads(response.body_as_unicode())
        
        item["paper_author"] = json_data["authors"]
        
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
