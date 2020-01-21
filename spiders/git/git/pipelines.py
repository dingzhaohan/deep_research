# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors

class GitPipeline(object):
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
        self.cursor.execute(self.sql,(item['git_star'], item['git_watch'], item['git_fork']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''insert into test(star, fork, watch) values(%s, %s, %s)'''
            return self._sql
        return self._sql

