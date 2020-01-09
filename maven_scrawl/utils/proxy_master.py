from random import choice

class ProxyMaster():
  def __init__(self):
    self.proxy_path = './assets/agent_ip.txt'
    self.proxyIP_list = self.getProxyIPList(self.proxy_path)
  
  # TODO: 考虑将这个方法提取为一个通用方法
  def getProxyIPList(self, proxy_path):
    f = open(proxy_path)
    line = f.readline()
    ip_list = []
    while line:
      ip_list.append(line.strip('\n'))
      line = f.readline()
    return ip_list

  # 获取一个随机代理IP
  def getRandomProxyIP(self):
    return choice(self.proxyIP_list)


# master = ProxyMaster()
# print(master.proxyIP_list)
# print(master.getRandomProxyIP())