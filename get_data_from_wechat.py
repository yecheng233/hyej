import sys
sys.path.append(r"C:\Users\ASUS\Desktop\航运e家\hyej_codestation")
import hyej_db_config

import datetime
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import json
import pandas as pd
import requests
import time
import schedule

# 获取access_token,access_token在2小时内有效
def get_token(appid,secret):
	headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
	url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%(appid)s&secret=%(secret)s'%{'appid':appid,'secret':secret}
	r = requests.get(url, headers= headers)
	print(r.text)
	
	access_token=json.loads(r.text)['access_token']
	return access_token


# 创建函数，从微信公众号后台获取相关表数据
def from_data_to_sql(tablename,data_type,date,access_token,):
	data=requests.post('https://api.weixin.qq.com/datacube/{}?access_token={}'.format(data_type,access_token),date)
	goal=json.loads(data.text)
	df=pd.DataFrame(goal['list'])   #返回一个数据框
	# 创建连接
	connect_info= 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_test_db_config  
	engine = create_engine(connect_info)
	df.to_sql(tablename,con=engine,if_exists='append',index=False)


if __name__ =="__main__":
	appid=hyej_db_config.wechat_public_config['appid']
	secret=hyej_db_config.wechat_public_config['secret']
	table_list=['getusersummary','getusercumulate','getarticlesummary']
	for j in range(-1,-2,-1):
	# 请求某日数据,默认是昨日
		day=(datetime.date.today() + datetime.timedelta(days=j)).strftime('%Y-%m-%d')
		print(day)
		date_send = json.dumps({"begin_date": str(day), "end_date": str(day)})
		# 遍历list去读取数据插入到mysql数据库
		# table_list=['getusersummary','getusercumulate','getarticlesummary','getuserread','getuserreadhour','getusershare','getusersharehour']
		for i in table_list:
			from_data_to_sql(i.replace('get','log_wechat_'),i,date_send,get_token(appid,secret))
			print(i.replace('get','log_wechat_') +"表插入成功~~~")
	print('wechat mission is ok')