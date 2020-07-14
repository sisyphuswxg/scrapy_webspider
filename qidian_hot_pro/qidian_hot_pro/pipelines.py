# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import pymongo
import redis


class QidianHotProPipeline(object):

    def process_item(self, item, spider):
        if item['form'] == '连载':
            item['form'] = "LZ"
        else:
            item['form'] = "WJ"

        return item


class MySQLPipeline(object):

    def open_spider(self, spider):
        db_name = spider.settings.get("MYSQL_DB_NAME", "qidian")
        host = spider.settings.get("MYSQL_HOST", "localhost")
        user = spider.settings.get("MYSQL_USER", "root")
        password = spider.settings.get("MYSQL_PASSWORD", "sisyphuswxg")
        self.db_conn = MySQLdb.connect(db=db_name,
                                       host=host,
                                       user=user,
                                       password=password,
                                       charset="utf8")
        self.db_cursor = self.db_conn.cursor()

    def process_item(self, item, spider):
        values = (item['name'], item['author'], item['type'], item['form'])
        sql = 'insert into qidian_hot(name, author, type, form) values (%s, %s, %s, %s)'
        self.db_cursor.execute(sql, values)
        return item

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_cursor.close()
        self.db_conn.close()


class MongoDBPipeline(object):

    def open_spider(self, spider):
        host = spider.settings.get("MONGODB_HOST", "localhost")
        port = spider.settings.get("MONGODB_PORT", 27017)
        db_name = spider.settings.get("MONGODB_NAME", "qidian")
        collection_name = spider.settings.get("MONGODB_COLLECTION", "qidian_hot")
        self.db_client = pymongo.MongoClient(host=host,
                                             port=port)
        self.db = self.db_client[db_name]
        self.collection = self.db[collection_name]

    def process_item(self, item, spider):
        item_dict = dict(item)
        self.collection.insert_one(item_dict)
        return item

    def close_spider(self, spider):
        self.db_client.close()


class RedisPipeline(object):

    def open_spider(self, spider):
        host = spider.settings.get("REDIS_HOST", "localhost")
        port = spider.settings.get("REDIS_PORT", 27017)
        db_index = spider.settings.get("REDIS_DB_INDEX", 0)
        password = spider.settings.get("REDIS_PASSWORD", "sisyphuswxg")
        self.db_conn = redis.StrictRedis(host=host,
                                         port=port,
                                         db=db_index,
                                         password=password)

    def process_item(self, item, spider):
        item_dict = dict(item)
        self.db_conn.rpush("novel", item_dict)
        return item

    def close_spider(self, spider):
        self.db_conn.connection_pool.disconnect()


