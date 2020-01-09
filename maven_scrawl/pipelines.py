# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

class MavenScrawlPipeline(object):
    def open_spider(self, spider):
        self.file_timetag = time.strftime('%Y%m%d_%H%M%S', time.localtime())

    def process_item(self, item, spider):
        itemDict = dict(item)
        print('[pipeline]', itemDict)

        # 将单条数据进行拼接（注意这里的分隔符的选择，必须选择独特的分隔符，否则无法区分项，这里不适合用空格做分隔符）
        itemStr = ''
        for val in itemDict.values():
            itemStr = itemStr + val + ' # '

        # 将单条数据写入txt
        with open('./dict/mvn_' + spider.time_tag + '.txt', 'a') as f:
            f.write(itemStr + '\n')
        return item
