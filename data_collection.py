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
connect_info= 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format('ye_test','bwmn0DKXCSGKktEf','rm-uf6mi05fl267li123to.mysql.rds.aliyuncs.com',3306, 'datastatistics')  
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


user='hangyunejia@163.com'
pasw='hangyunejia2019'
auth_token=authorize(user,pasw)


# 从友盟拉取数据到数据库
def get_data_from_umneng():
	auth_token=authorize(user,pasw)
# 打开app列表
# apps(auth_token)
	day=(datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
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

	print("umneng mission is ok")




# 从正式库拉取数据到测试库
# 建立连接
connect_begin= 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format('ye_test','bwmn0DKXCSGKktEf','rm-uf6mi05fl267li123to.mysql.rds.aliyuncs.com',3306, 'datastatistics')  
engine_test = create_engine(connect_begin)


connect_end= 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format('ye_online','waItthn8KAmI5cVO','rm-uf6mi05fl267li123to.mysql.rds.aliyuncs.com',3306, 'hyej')  
engine_formal = create_engine(connect_end)
	

def transfer_between_db(begin,end,table_name):
    sql="""select * from `%(tablename)s` where created_at between '%(begin_time)s' and '%(end_time)s'""" %{'tablename':table_name,'begin_time':(datetime.date.today()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d %T'),'end_time':datetime.date.today().strftime('%Y-%m-%d %T')}
    print(sql)
    df=pd.read_sql(sql,con=begin)
    df.to_sql(table_name,con=end,if_exists='append',index=False)
    print(table_name+' is ok,please check your data in your database')

order='order'
member='member'
member_cv='member_cv'
member_tree='member_tree'

def get_data_from_mysql():
    print("Today is "+(datetime.date.today()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d %T'))
    transfer_between_db(engine_formal,engine_test,member)
    transfer_between_db(engine_formal,engine_test,order)
    transfer_between_db(engine_formal,engine_test,member_cv)
    transfer_between_db(engine_formal,engine_test,member_tree)
    
    print("mysql mission is ok")
    
    
    

# 获取access_token,access_token在2小时内有效
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxa295abed1732bc60&secret=fa210301143e48d2b95a0cbc0c286709'
r = requests.get(url, headers= headers)
access_token=json.loads(r.text)['access_token']

# 创建函数，从微信公众号后台获取相关表数据
def from_data_to_sql(tablename,data_type,date,access_token):
    try:
        data=requests.post('https://api.weixin.qq.com/datacube/{}?access_token={}'.format(data_type,access_token),date)
        goal=json.loads(data.text)
        df=pd.DataFrame(goal['list'])
        df.to_sql(tablename,con=engine,if_exists='append',index=False)
    except:
        print("Something was wrong")



def get_data_from_wechat():
	# 调用之前的准备，注意，每日的请求次数是有上限的
	# 昨天的时间，作为全局变量
	day=(datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
	date_send = json.dumps({"begin_date": str(day), "end_date": str(day)})

	# 遍历list去读取数据插入到mysql数据库
#    ,'getuserread','getuserreadhour','getusershare','getusersharehour'
	table_list=['getusersummary','getusercumulate','getarticlesummary']
	for i in table_list:
		from_data_to_sql(i.replace('get','log_wechat_'),i,date_send,access_token)
		print(i.replace('get','log_wechat_') +"表插入成功~~~")
	print('wechat mission is ok')

# 任务调度
if __name__ =="__main__":
    print("Let's run,run,run......")
    schedule.every().day.at("09:43").do(get_data_from_umneng)
    schedule.every().day.at("09:43").do(get_data_from_mysql)
    schedule.every().day.at("09:43").do(get_data_from_wechat)  
    while True:
        schedule.run_pending()
        time.sleep(60)