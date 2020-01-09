# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MavenScrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LibItem(scrapy.Item):
    # 分类名
    category = Field()
    # 库名
    libName = Field()
    # GroupId
    groupId = Field()
    # artifactId
    artifactId = Field()
    # 库总使用数
    libUsages = Field()
    # 库版本
    version = Field()
    # 库使用数
    usages = Field()
    # 库版本时间
    date = Field()
