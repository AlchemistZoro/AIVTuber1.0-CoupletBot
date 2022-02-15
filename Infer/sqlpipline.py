
import pymysql
import argparse
import time
from danmu import Danmu,ProxyGet
import uuid


from datetime import datetime



MYSQL_DBNAME=''
MYSQL_HOST=''
MYSQL_USER= ''
MYSQL_PASSWD= ''
MYSQL_PORT= 3306



def InsertDanmu(data,cursor,conn):
    # data = dict(item)
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'insert ignore into %s (%s) values (%s)' % ('MyLiveDanmu', keys, values)
    cursor.execute(sql, tuple(data.values()))
    conn.commit()


class SQLpipline():
    def __init__(self):
        self.startconnect()
    def startconnect(self):
        self.conn = pymysql.connect(
            host=MYSQL_HOST, 
            user=MYSQL_USER, 
            password=MYSQL_PASSWD, 
            database=MYSQL_DBNAME,
            port=MYSQL_PORT
            )   
        self.cursor = self.conn.cursor()
    def endconnect(self):
        self.cursor.close()
        self.conn.close()
    def get_text_in(self):

        sql="SELECT * FROM %s WHERE state_code=200 AND roomid=22274371  ORDER BY timeline  DESC LIMIT 1;" % ('MyLiveDanmu')

        search_count=self.cursor.execute(sql)
        try:
            danmu=self.cursor.fetchall()[0]
            text_in=danmu[3]
            hash_id=danmu[0]
            user_name=danmu[2]
            self.conn.commit()

        except:
            self.conn.commit()
            return '','',0

        return text_in,user_name,hash_id

    def process_text_out(self,hash_id,text_out,date_time):
  
        sql="UPDATE MyLiveDanmu  SET review_timeline='%s' ,state_code=100,review_text='%s' WHERE hashid='%s';" % (date_time,text_out,hash_id)
        self.cursor.execute(sql)
        self.conn.commit()


if __name__ == "__main__":
    sqlp=SQLpipline()
    while 1:
        print(sqlp.get_text_in())
        time.sleep(1)
    # hash_id='9864b5cb2b8ce2f064d5c281bd13392f'
    # text='lalalalallala'
    
    # now = datetime.now()
    # date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # # print(date_time)
    # sqlp.process_text_out(hash_id,text,date_time)
    
    