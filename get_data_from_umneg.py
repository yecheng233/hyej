import sys
sys.path.append(r"C:\Users\ASUS\Desktop\航运e家\hyej_codestation")
import hyej_db_config
import sql_doc


import datetime
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import json
import pandas as pd
import requests
import time
import schedule

# 建立连接
connect_info='mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_test_db_config   
engine = create_engine(connect_info)


#获取auth_token
def authorize(user, pasw):
    url = 'http://api.umeng.com/authorize'
    body = {'email': "%s"%(user), 'password': '%s'%(pasw)}
    response = requests.post(url, params = body)
    return response.json()['auth_token']

#获取今日的基本数据
def base_data(appkey,date,auth_token):
    url = 'http://api.umeng.com/base_data?appkey=%s&date=%s&auth_token=%s'%(appkey,date,auth_token)
    response = requests.get(url)
    return response.json()


#获取渠道用户数据
def active_users(appkey,auth_token,date,per_page):
    url = 'http://api.umeng.com/channels?appkey=%s&auth_token=%s&date=%s&per_page=%s'%(appkey,auth_token,date,per_page)
    response = requests.get(url)
    return response.json()



if __name__ =="__main__":
    for j in range(-1,-2,-1):
        day=(datetime.date.today() + datetime.timedelta(days=j)).strftime('%Y-%m-%d')
        print(day)
        user=hyej_db_config.Umeng_config['user']
        pasw=hyej_db_config.Umeng_config['password']
        auth_token=authorize(user,pasw)
        plat_form={'andriod':'5760ba5a67e58ed055000727','ios':'577a03e567e58ed540000280'}
        # 插入渠道数据
        for k,v in plat_form.items():
            df=pd.DataFrame(active_users(v,auth_token,day,100))
            df['platform']=k
            df.to_sql('umneg_channels',con=engine,if_exists='append',index=False)

        # 插入日数据
        for k,v in plat_form.items():
        	df=pd.DataFrame.from_dict(base_data(v,day,auth_token),orient='index').T
        	df['platform']=k
        	df.to_sql('umneg_appdata',con=engine,if_exists='append',index=False)

    print("umneg mission is ok")


