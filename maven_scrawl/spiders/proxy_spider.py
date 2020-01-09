import scrapy
from maven_scrawl.custom_settings import proxy_settings

class ProxySpider(scrapy.Spider):
  name = 'proxy'
  start_urls = [ 'http://www.66ip.cn/1.html' ]
  custom_settings = proxy_settings.settings

  def parse(self, response):
    print('proxy', response.status, response.headers.getlist('Set-Cookie'))
    ip_list = response.css('div.containerbox tr:not(first-child) td:first-child::text').extract()
