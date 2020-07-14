# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re
from scrapy.exceptions import DropItem


class FilterPipeline(object):
    def process_item(self, item, spider):
        # area
        item["area"] = re.findall("\d+\.?\d*", item["area"])[0]
        # unit price
        item["unit_price"] = re.findall("\d+\.?\d*", item["unit_price"])[0]
        if item["direction"] == "暂无数据":
            raise DropItem("房屋朝向无数据，抛弃此项目: %s" % item)
        return item


class CSVPipeline(object):
    index = 0
    file = None

    # Spider开启时，执行打开文件操作
    def open_spider(self, spider):
        # 以追加形式打开文件
        self.file = open("home.csv", "a", encoding="utf-8")

    # 数据处理
    def process_item(self, item, spider):
        # 第一行写入列名
        if self.index == 0:
            column_name = "name,type,area,direction,fitment,elevator,total_price,unit_price,property\n"
            # 将字符串写入到文件中
            self.file.write(column_name)
            self.index = 1
        # 获取item中各个字段，将其连接成一个字符串
        # 字段之间用逗号隔开
        # 反斜杠用于连接下一行的字符串
        # 字符串末尾要有换行符\n
        home_str = item['name'] + "," + \
                   item["type"] + "," + \
                   item["area"] + "," + \
                   item["direction"] + "," + \
                   item["fitment"] + "," + \
                   item["elevator"] + "," + \
                   item["total_price"] + "," + \
                   item["unit_price"] + "," + \
                   item["property"] + "\n"
        # 将字符串写入到文件中
        self.file.write(home_str)
        return item

    # Spider关闭时，执行关闭文件操作
    def close_spider(self, spider):
        self.file.close()
