
"""
Created on Mon Jun 24 10:05:26 2019
@author: yecheng
"""
import sys
sys.path.append(r"F:\config")
import hyej_db_config
import sql_doc
import datetime
import pymysql
import sqlalchemy
from sqlalchemy import create_engine

# 邮件模块
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
import smtplib

import time
import pandas as pd

def get_data_to_excelfile(yoursql,path):
	connect_info='mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_test_db_config 
	engine = create_engine(connect_info)
	df=pd.read_sql(yoursql,con=engine)
	df.to_excel(path)



def send_mail(fp):
	

	msg = MIMEMultipart('related')
	msg['subject']=(datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y%m%d')+"客服添加数据列表"
	msg['from'] = 'yecheng@xiaozhoukeji.net'
	msg['to']="""yecheng@xiaozhoukeji.net,
	wuchenghao@xiaozhoukeji.net"""



	# 带上附件
	att1 = MIMEBase('application', 'octet-stream')
	att1.set_payload(open(fp, 'rb').read())
	att1.add_header('Content-Disposition', 'attachment', filename=('gbk', '', fp.split("\\")[-1]) )
	encoders.encode_base64(att1)
	msg.attach(att1)


    #发送
	try:
		server =smtplib.SMTP_SSL('smtp.exmail.qq.com',port=465)
		server.connect('smtp.exmail.qq.com')
		# server.starttls()
		server.login('yecheng@xiaozhoukeji.net', 'Lhi9X6p3NozrfUD9')  # XXX为用户名，XXXXX为密码
		server.sendmail(msg['from'],msg['to'].split(','),msg.as_string())
		#                         ,msg['to'].split(','),msg.as_string())
		server.quit()
		print('邮件发送成功:'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	except Exception as e:
		print(str(e))




if __name__ =="__main__":
	path=r'C:\Users\ASUS\Desktop\航运e家\文献研究\客服添加数据'+str((datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d'))+'.xlsx'
	print(path)
	get_data_to_excelfile(sql_doc.daily_kf_wechatlist,path)
	send_mail(path)
	print("ok")




