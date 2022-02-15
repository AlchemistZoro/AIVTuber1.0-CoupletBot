import pymysql
import argparse
import time
from danmu import Danmu,ProxyGet
import uuid
from tcheck import IsToxic

createTableLiveDanmu='''
create table if not exists MyLiveDanmu(
    hashid varchar(64) primary key,
    roomid varchar(16),
    nickname varchar(64),
    text varchar(128),
    uid varchar(16),
    timeline varchar(32),
    review_timeline varchar(32),
    state_code int(10),
    review_text varchar(128)
    )default character set = 'utf8';'''


def CreateTable(cursor,conn,sql):
    cursor.execute(sql)
    conn.commit()



def InsertDanmu(data,cursor,conn):
    # data = dict(item)
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'insert ignore into %s (%s) values (%s)' % ('MyLiveDanmu', keys, values)
    cursor.execute(sql, tuple(data.values()))
    conn.commit()


def ProcessLiveInfo(MYSQL_DBNAME='liveDanmu',MYSQL_HOST='localhost',MYSQL_USER= 'root',MYSQL_PASSWD= '123456',MYSQL_PORT= 3306):
   
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWD, database=MYSQL_DBNAME,
                                  port=MYSQL_PORT)
    
    cursor = conn.cursor()

    CreateTable(cursor,conn,createTableLiveDanmu)


    proxy_url='http://127.0.0.1:5555/'
    # roomid='7688602'
    roomid='22274371'
    
    bDanmu = Danmu(roomid)
    proxy_get=ProxyGet(proxy_url)
    
    hash_previous_list=[]
    while 1:
        danmu_list,hash_list=bDanmu.get_danmu(proxy_get)
        for danmu in  danmu_list:
            if danmu['hashid'] not in hash_previous_list:
                print(danmu)
                danmu['roomid']=roomid
                danmu['review_timeline']=str('')
                danmu['state_code']=int(404) if IsToxic(danmu['text']) else int(200)
                danmu['review_text']=str('')
                InsertDanmu(danmu,cursor,conn)
                time.sleep(0.5)
        hash_previous_list=hash_list 
        time.sleep(1)
    
    # print('finishi video :'+vbid)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    
    
    time_start=time.time()
    ProcessLiveInfo()
    time_end=time.time()
    print(time_end-time_start)
 
    
