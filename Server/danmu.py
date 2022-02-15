# -*- encoding: utf-8 -*-
#@time:  2020/11/15 22:54
#@author: chenTao
#@file:  dnmu.py
 
from weakref import proxy
import requests
import time
import io,sys
import hashlib
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
    def __init__(self,roomid):
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        # 请求头
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        
        }
        self.roomid=roomid
        # 定义POST传递的参数
        # 我的roomid 22274371
        self.data = {
            'roomid': self.roomid
        }

 
    def get_danmu(self,getProxy):
        
        html=''
        for i in range(5):
            proxy_request=getProxy.get_radom_proxy()
            proxy_dict={"http":proxy_request}
            state_code=requests.post(url=self.url, headers=self.headers, data=self.data,proxies=proxy_dict).status_code
            if state_code==200:
                # 获取直播间弹幕
                html = requests.post(url=self.url, headers=self.headers, data=self.data,proxies=proxy_dict).json()
                break
            print('无法获得弹幕，请求被拦截')
        # 解析弹幕列表
        danmu_list=[]
        hash_list=[]
        for content in html['data']['room']:
  
            danmu_dict={
                'nickname':content['nickname'],
                'text':content['text'],
                'uid':content['uid'],
                'timeline':content['timeline']               
            }
            idx=content['nickname']+content['text']+content['timeline']
            hash_id=hashlib.md5(idx.encode('utf-8')).hexdigest()
            danmu_dict['hashid']=hash_id
            hash_list.append(hash_id)
            danmu_list.append(danmu_dict)         
        return danmu_list,hash_list

def main(proxy_url='http://127.0.0.1:5555/',roomid='7688602'):
    bDanmu = Danmu(roomid)
    proxy_get=ProxyGet(proxy_url)
    danmu_list=bDanmu.get_danmu(proxy_get)
    return danmu_list

if __name__ == '__main__':
    print(main())

    