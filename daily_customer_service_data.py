# 从文件夹中导入写好的配置文件，这样即便同步代码也不要紧
import sys
sys.path.append(r"F:\config")
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

def send2robot(Webhook,content):
    headers={'Content-Type': 'application/json'}
    post_data={
            "msgtype": "text",
            "text": {"content": content},
            "mentioned_list":["@all","叶成"],   #这个mentioned_list好像没什么用
    		"mentioned_mobile_list":["13761849216","@all"]   #获取不到user_id时，提醒对应手机号码的用户
    }
    
    requests.post(Webhook,json.dumps(post_data), headers=headers)
    print("消息发送成功！")


def get_content(sql,sample):
	connect_info= 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_db_config
	engine = create_engine(connect_info)
	df=pd.read_sql(sql,con=engine)
	m=df.to_dict(orient='index')
	content=[]
	for k,v in m.items():
		content.append(sample%v)
	msg=";\n".join(content)
	return msg


def get_test_content(sql,sample):
	connect_info= 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_test_db_config
	engine = create_engine(connect_info)
	df=pd.read_sql(sql,con=engine)
	m=df.to_dict(orient='index')
	content=[]
	for k,v in m.items():
		content.append(sample%v)
	msg=";\n".join(content)
	return msg


if __name__ =="__main__":
	# 客服机器人003
	robot_customer_service='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=73fdbd23-6101-4628-a316-553239b624d2'
	sample="""
客服小姐姐--%(wechat_name)s:
	日期 %(date_day)s
	好友总数 %(total)s
	好友增加数 %(increase_num)s,其中添加好友通过数 %(add_adopt_num)s,被添加人数 %(added_num)s
	好友减少数 %(reduce_num)s
	聊天人数 %(chat_num)s"""



	VipSummary="""Hi,morning.
	日期:%(d)s
	企业用户登录数:%(company_login_cnt)s
	新增领取VIP数:%(vip_pay_cnt)s
	当日发布职位的企业总数量:%(job_publish_company_cnt)s
	当日发布的职位总数:%(job_cnt)s
	当日vip企业发布的职位总数:%(vip_job_cnt)s
	当日发布职位的vip企业数量:%(vip_company_cnt)s
	当日船员联系企业的认证船员数量:%(crew_2_company_distinct_cnt)s
	当日船员联系企业的总次数:%(company_2_crew_cnt)s
	当日vip企业联系船员的vip企业数量:%(vipCompany_2_crew_distinct_cnt)s
	当日vip企业联系船员的总次数:%(vipCompany_2_crew_cnt)s
	"""
	
	msg=get_content(sql_doc.daily_kf_report,sample)
	print(msg)
	send2robot(robot_customer_service,msg)

	msg_vip_summary=get_test_content(sql_doc.daily_vip_sumary,VipSummary)
	print(msg_vip_summary)
	send2robot(robot_customer_service,msg_vip_summary)
	


	# 不刷单时，可以放开此处
	# con="""分配数据已邮件吴老轨，请查收"""
	# print(con)
	# send2robot(robot_customer_service,con)


