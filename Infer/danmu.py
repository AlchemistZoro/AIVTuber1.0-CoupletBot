# -*- encoding: utf-8 -*-
#@time:  2020/11/15 22:54
#@author: chenTao
#@file:  dnmu.py
 
from weakref import proxy
import requests
import time
import io,sys
  
# sys.setdefaultencoding('utf8')   

# import
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

class ProxyGet():
    def __init__(self,url):
        self.url=url
    def get_radom_proxy(self):
        proxy=requests.get(self.url+'random').text
        return proxy
    def get_proxy_number(self):
        number=requests.get(self.url+'count').text
        return number
class Danmu():
    def __init__(self):
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        # 请求头
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            
        }
        # 定义POST传递的参数
        # 我的roomid 22274371
        self.data = {
            'roomid': '22274371'
        }
        self.proxy={"http":'120.26.212.253:3128'}
 
    def get_danmu(self):
        # 获取直播间弹幕
        html = requests.post(url=self.url, headers=self.headers, data=self.data,proxies=self.proxy).json()
        # 解析弹幕列表
        danmu_list=[]
        for content in html['data']['room']:
            danmu_dict={
                'nickname':content['nickname'],
                'text':content['text'],
                'uid':content['uid'],
                'timeline':content['timeline']               
            }
            danmu_list.append(danmu_dict)         
        return danmu_list
 
if __name__ == '__main__':
    # 创建bDanmu实例
    bDanmu = Danmu()
    i = 1

    print(bDanmu.get_danmu())
    # url='http://127.0.0.1:5555/'
    # proxy_get=ProxyGet(url)
    # use_proxy=proxy_get.get_radom_proxy()
    # print(use_proxy)
 