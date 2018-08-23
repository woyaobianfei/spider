# -*- coding: utf-8 -*-
import pymongo
from iqiyi.settings import mongo_db_collection,mongo_db_name,mongo_port,mongo_host
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from iqiyi.items import DeviceDistributionItem
from iqiyi.spiders import iqiyi

class IqiyiPipeline(object):

    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        sheetname = mongo_db_collection
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item

    # 删除mongodb中的对应的数据
    def remove_item(self, item, key_name, name):
        self.post.remove({'key_name': key_name, 'name': name})
        print("删除key_name : " + key_name + " 剧集名称: " + name + " 成功")
        return item

    # 删除mongodb中的对应的数据
    def remove_aid_item(self, item, key_name, aid):
        # 这里必须要用单引号！！
        self.post.remove({'key_name': key_name, 'aid': aid})
        print("删除key_name : " + key_name + " aid: " + aid + " 成功")
        return item



































# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect(host="localhost", user="root", password="123456", db="iqiyi", port=3306, charset="utf8m64")
#         self.cursor = self.conn.cursor()
#
#     def process_item(self,item, spider):
#         # insert_sql = """ insert into iqiyi.video_play_device_distribution(aid,name,mobile_terminal,pc_terminal)
#         #                  values(%s, %s, %s, %s) """
#         # try:
#         #     self.cursor.execute(insert_sql, (item['aid'], item['name'], item['mobile_terminal_distribution'], item['pc_device_distribution']))
#         #     self.conn.commit()
#         #
#         # except Exception as e:
#         #     # 错误回滚
#         #     self.conn.rollback()
#         # finally:
#         #     self.conn.close()
#         # insert_sql, params = item.get_insert_sql()
#
#     def do_insert(self, cursor, item):
#         # 执行具体的插入
#         # 根据不同的item 构建不同的sql语句并插入到mysql中
#         insert_sql, params = item.get_insert_sql()
#         cursor.execute(insert_sql, params)
