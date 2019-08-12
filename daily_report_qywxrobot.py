
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
import schedule
import time

# 利用机器人向指定群发送消息
def send2robot(Webhook,content):
    headers={'Content-Type': 'application/json'}
    post_data={
            "msgtype": "text",
            "text": {
                "content": content
            }}
    requests.post(Webhook,json.dumps(post_data), headers=headers)



def get_content(yoursql):
		# 建立连接，配置信息在hyej_db_config.py文件中
	connect_info='mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_test_db_config 
	engine = create_engine(connect_info)
	
	df=pd.read_sql(yoursql,con=engine)
	report_dict=df.to_dict(orient='index')[0]
	return report_dict



if __name__ =="__main__":
	print("your mission is running~~~")
	# 主群机器人
	robot_daily_report='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=685da879-5ddf-4ada-b728-205983fbabc2'
	# 默认发送文本样式
	sample_daily="""Hi,morning!
	%(date)s数据日报
	App日活：%(dau)d
	APP新增激活：%(new_lauch)d
	注册用户：新增%(new_member_cnt)d,累计%(total_member)d（注册率%(enrollment_rate).2f%%）
	认证用户：新增%(new_certify_cnt)d,累计%(total_crew)d（认证率%(certified_rate).2f%%）
	订单：%(order_person_cnt)d人,%(order_cnt)d笔,当日注册转化订单人数%(today_pay_cnt)d，当日付费转化率%(today_pay_rate).2f%%（培训%(train_cnt)d，办证%(certified_cnt)d，体检%(exam_cnt)d）
	流水：%(order_amt)d元（培训%(train_amt)d元，办证%(certified_amt)d元，体检%(exam_amt).2f元）
	Arppu：%(arpu)d元
	公众号粉丝：增粉%(new_fans)s,取关%(cancel_fans)s,累计%(total_fans)s
	合伙人：当日%(partner_use)s人参与拉新，新增注册%(partner_new_member_cnt)s，新增认证%(partner_new_certify_cnt)s（认证率%(partner_certified_rate).2f%%）
	"""
	content=sample_daily%get_content(sql_doc.daily_robot_report)
	print(content)
	
	sample_weekly="""Hi,today is Monday,so let's we have a quick view of our job about last week.
	数据周报
	app周活:1234（+23%）
	app新增周活：
	"""






	send2robot(robot_daily_report,content)
    
    # schedule.every().day.at("10:30").do(job_data_reporter,)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)