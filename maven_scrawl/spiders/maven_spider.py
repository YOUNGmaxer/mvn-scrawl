import scrapy
import re
import os
import time
from maven_scrawl.items import LibItem
from maven_scrawl.custom_settings import maven_settings

class MavenSpider(scrapy.Spider):
  name = 'maven'
  page_init = 1
  page_len = 10
  lib_limited = 3
  cate_link_path = './dict/cate_link'
  lib_link_path = './dict/lib_link'
  # 爬虫运行时间标识（用于文件读写时）
  time_tag = time.strftime('%Y%m%d_%H%M%S', time.localtime())
  # 记录当前的代理IP（用来避免没必要的频繁更换代理IP）
  cur_proxy = None
  url_base = 'https://mvnrepository.com'
  custom_settings = maven_settings.settings

  def start_requests(self):
    urls = []
    for page in range(self.page_init, self.page_len + 1):
      url = f'https://mvnrepository.com/open-source?p={page}'
      urls.append(url)
    self.log(urls)
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  # 解析分类列表页
  def parse(self, response):
    # 分类链接列表
    cate_href_list = response.xpath('//div[@id="maincontent"]/div/h4/a/@href').extract()
    # 分类名称
    cate_title_list = response.xpath('//div[@id="maincontent"]/div/h4/a/text()').extract()
    # print('[parse]', cate_href_list, cate_title_list)

    # 对本次分类链接进行保存
    self.saveLinks(self.cate_link_path, cate_href_list)

    # 分类链接
    for index in range(len(cate_href_list)):
      url = self.url_base + cate_href_list[index]
      cate_title = cate_title_list[index]
  
      yield scrapy.Request(url=url, callback=self.parse_cate, meta={'cate_title': cate_title})

  # 解析分类详情页（依赖列表页）
  def parse_cate(self, response):
    # 取第一页依赖库
    lib_title_list = response.xpath('//div[@class="im"]//h2[@class="im-title"]/a[not(@class="im-usage")]/text()').extract()
    lib_href_list = response.xpath('//div[@class="im"]//h2[@class="im-title"]/a[not(@class="im-usage")]/@href').extract()
    lib_usages_list = response.xpath('//div[@class="im"]//h2[@class="im-title"]/a[@class="im-usage"]/b/text()').extract()
    # print('[parse_cate]', lib_title_list, lib_usages_list)
    # print('[parse_cate] response', response.headers)
    # print('[parse_cate] response', response.Request.headers)

    # 取前 n 个依赖库
    lib_title_list = lib_title_list[0:self.lib_limited]
    lib_href_list = lib_href_list[0:self.lib_limited]
    lib_usages_list = lib_usages_list[0:self.lib_limited]

    # 对本次依赖库链接进行保存
    self.saveLinks(self.lib_link_path, lib_href_list)

    cate_title = response.meta['cate_title']
    # print('!!!parse_cate!!!', cate_title, response.url, lib_title_list)

    # 依赖库链接
    for index in range(len(lib_href_list)):
      lib_href = lib_href_list[index]
      lib_usages = lib_usages_list[index]
      lib_title = lib_title_list[index]
      url = self.url_base + lib_href
      yield scrapy.Request(url=url, callback=self.parse_lib,
        meta={
          'cate_title': cate_title,
          'lib_usages': lib_usages,
          'lib_title': lib_title,
          'lib_href': lib_href
        })

  def parse_lib(self, response):
    version_list = response.xpath('//table[contains(@class, "versions")]/tbody//td/a[contains(@class, "vbtn")]/text()').extract()
    # usages_list = response.css('table.versions tr td:nth-last-child(2) > a::text').extract()
    # 这里需要考虑两种情况，一种是 usages 为0的情况，此时没有a标签；一种是不为0的情况，此时有a标签
    usages_list = response.css('table.versions tr td:nth-last-child(2)').re(r'<td>\s*(\d*)|(\d*)</a>')
    date_list = response.css('table.versions tr td:last-child::text').extract()

    # 去除数组中的空字符
    while '' in usages_list:
      usages_list.remove('')

    lib_href = response.meta['lib_href']
    lib_href = lib_href.split('/')

    for index in range(len(version_list)):
      item = LibItem()
      item['category'] = response.meta['cate_title']
      item['libName'] = response.meta['lib_title']
      item['groupId'] = lib_href[2]
      item['artifactId'] = lib_href[3]
      item['libUsages'] = response.meta['lib_usages']
      item['version'] = version_list[index]
      item['usages'] = usages_list[index]
      item['date'] = date_list[index]
      yield item
  
  def saveLinks(self, path, link_list):
    f = open(path + '_' + self.time_tag + '.txt', 'a')
    for href in link_list:
      url = self.url_base + href
      f.write(url + '\n')
    f.close()