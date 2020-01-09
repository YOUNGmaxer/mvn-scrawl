import random
import logging
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from maven_scrawl.utils.proxy_master import ProxyMaster

logger = logging.getLogger(__name__)
proxyMaster = ProxyMaster()

# 注意在本项目中，如果不手动设置 User-Agent，请求到的页面不一致
class RandomUserAgentMiddleware():
  def __init__(self):
    self.user_agents = [
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
      "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
      "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
      "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
      "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
      "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
      "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]

  def process_request(self, request, spider):
    request.headers['User-Agent'] = random.choice(self.user_agents)

class HeaderWatcher():
  def process_request(self, request, spider):
    # print('[HeaderWatcher]', request.headers)
    return None

class SuccessMiddleware():
  def process_response(self, request, response, spider):
    cur_url = response.url
    tag4Cate = 'open-source/'
    tag4Lib = 'artifact/'
    file4Cate = './dict/cate_link_used'
    file4Lib = './dict/lib_link_used'
    if response.status == 200:
      if tag4Cate in cur_url:
        self.writeUrl(file4Cate, cur_url, spider)
      if tag4Lib in cur_url:
        self.writeUrl(file4Lib, cur_url, spider)
    return response
  
  def writeUrl(self, path, url, spider):
    f = open(path + '_' + spider.time_tag + '.txt', 'a')
    f.write(url + '\n')
    f.close()



class LocalRetryMiddleware(RetryMiddleware):
  def process_request(self, request, spider):
    # print('[LocalRetryMiddleware]', request.headers)
    return None

  def process_response(self, request, response, spider):
    if response.status == 403:
      logger.debug('[LocalRetry] 403警告')
      return self._retry(request, response.status, spider) or response
    return super().process_response(request, response, spider)

class ProxyMiddleware():
  def process_request(self, request, spider):
    if spider.cur_proxy:
      request.meta['proxy'] = spider.cur_proxy
    if request.meta.get('retry_times'):
      ip = proxyMaster.getRandomProxyIP()
      print('[ProxyMiddleware]', f'获取代理ip为 {ip}')
      if ip:
        ip = f'http://{ip}'
        # 这里设置请求的代理IP
        request.meta['proxy'] = ip
        spider.cur_proxy = ip
        print('[ProxyMiddleware]', f'设置代理ip为 {ip}')

class CookieMiddleware():
  def process_response(self, request, response, spider):
    print('cookie-middleware', response.status, response.headers.getlist('Set-Cookie'))
    if response.status == 521:
      cookie = response.headers.getlist('Set-Cookie')
      # TODO: 完成此处 cookie 逻辑，以便成功访问网站
      if cookie:
        cookie = cookie[0].split(';')
        print('cookie-middleware', 'cookie', cookie)
    return response