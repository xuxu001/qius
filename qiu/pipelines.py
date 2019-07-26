# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class QiuPipeline(object):




    def __init__(self):
        dbparams={
            'host':'127.0.0.1',
            'port':3306,
            'user':'ceshi001',
            'password':'ceshi001',
            'database':'jianshu',
            'charset':'utf8mb4'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['name'],item['funny'],item['comment'],item['img'],
                                      item['content']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql="""
            insert into qiu(id,name,funny,comment,img,content)values(null,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql