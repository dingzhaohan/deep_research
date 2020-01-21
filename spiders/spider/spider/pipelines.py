# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors

class SpiderPipeline(object):
	def __init__(self):
		dbparams = {
			'host':'123.57.37.103',
            'port':3306,
            'user':'root',
            'password':'root',
            'database':'deep_research',
            'charset':'utf8'
		}
		self.conn = pymysql.connect(**dbparams)
		self.cursor = self.conn.cursor()
		self._sql = None

	def process_item(self, item, spider):
		self.cursor.execute(self.sql,(item["paper_title"],
										 ','.join(item["paper_author"]),
										 item["paper_abstract"],
										 item["git_star"],
										 item["git_watch"],
										 item["git_fork"],
										 item["git_readme_size"],
    									 item["git_open_issues_count"],
    									 item["git_repo_created_time"],
    									 item["ppc_star"],
    									 ','.join(item["ppc_codeframe"]),
    									 ','.join(item["ppc_tasks_classification"]),
    									 ','.join(item["ppc_all_repo_address"]),
    									 item["ppc_arxiv_address"],
    									 item["ssr_citation"],
    									 ','.join(item["ssr_tasks_classification"]),
    									 ','.join(item["ssr_img_address"]),
    									 item["ssr_img_count"],
    									 item["ssr_influence"],
    									 item["ssr_venue"],
    									 item["ssr_paper_submit_year"]))
		self.conn.commit()
		return item

	@property
	def sql(self):
		if not self._sql:
			self._sql = '''insert into website(paper_title,paper_author,paper_abstract,git_star,git_watch,git_fork,git_readme_size,git_open_issues_count,git_repo_created_time,ppc_star,ppc_codeframe,ppc_tasks_classification,ppc_all_repo_address,ppc_arxiv_address,ssr_citation,ssr_tasks_classification,ssr_img_address,ssr_img_count,ssr_influence,ssr_venue,ssr_paper_submit_year) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
			return self._sql
		return self._sql

