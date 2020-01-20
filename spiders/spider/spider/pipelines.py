# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb


class SpiderPipeline(object):

	def __init__():
		self.conn = MySQLdb.connect(
			host = '123.57.37.103',
			port = 3306,
			user = 'root',
			password = '87793faa',
			charset = 'utf8',
			db = 'deep_research'
			)
    def process_item(self, item, spider):
    	self.save(item)
        return item

    def save(self, item):
    	sql = '''insert int website(paper_title,
    								paper_author,
    								paper_abstract,
    								git_star,
    								git_watch,
    								git_fork,
    								git_readme_size,
    								git_open_issues_count,
    								git_repo_created_time,
    								ppc_star,
    								ppc_codeframe,
    								ppc_tasks_classification,
    								ppc_all_repo_address,
    								ppc_arxiv_address,
    								ssr_citation,
    								ssr_tasks_classification,
    								ssr_img_address,
    								ssr_img_count,
    								ssr_influence,
    								ssr_venue,
    								ssr_paper_submit_year,
    								model_input,
    								model_output,
    								datasets,
    								datasets_public,
    								model_reach_sota,
    								optimize_method,
    								docker_image,
    								code_language,
    								code_version,
    								pretrained_model,
    								network_arch)VALUES(
    								%s, %s, %s, %d, %d, %d,
    								%d, %d, %s, %d, %s, %s,
    								%s, %s, %d, %s, %s, %d,
    								%d, %s, %s, %s, %s, %s,
    								%s, %s, %s, %s, %s, %s,
    								%s, %s, %s'''
    	self.conn.cursor().execute(sql, [item["paper_title"],
    									 item["paper_author"],
    									 item["paper_abstract"],
    									 item["git_star"],
    									 item["git_watch"],
    									 item["git_fork"],
    									 item["git_readme_size"],
    									 item["git_open_issues_count"],
    									 item["git_repo_created_time"],
    									 item["ppc_star"],
    									 item["ppc_codeframe"],
    									 item["ppc_tasks_classification"],
    									 item["ppc_all_repo_address"],
    									 item["ppc_arxiv_address"],
    									 item["ssr_citation"],
    									 item["ssr_tasks_classification"],
    									 item["ssr_img_address"],
    									 item["ssr_img_count"],
    									 item["ssr_influence"],
    									 item["ssr_venue"],
    									 item["ssr_paper_submit_year"],
    									 item["model_input"],
    									 item["model_output"],
    									 item["datasets"],
    									 item["datasets_public"],
    									 item["model_reach_sota"],
    									 item["optimize_method"],\
    									 item["docker_image"],
    									 item["code_language"],
    									 item["code_version"],
    									 item["pretrained_model"],
    									 item["network_arch"]])
    	self.conn.commit()
