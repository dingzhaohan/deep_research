# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class GitPipeline(object):
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
    	sql = '''insert into test(paper_title, star, fork, watch)VALUES(%s, %d, %d, %d)'''
    	self.conn.cursor().execute(sql, [item["paper_title"], item["git_star"], item["git_fork"], item["git_watch"]])
    	self.conn.commit()

