# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 10:05:26 2019

@author: yecheng
"""
import sys
sys.path.append(r"C:\Users\ASUS\Desktop\航运e家\hyej_codestation")
import hyej_db_config
import sql_doc
import datetime
import pymysql
import sqlalchemy
from sqlalchemy import create_engine

import time
import schedule
import pandas as pd


# 建立连接
connect_begin='mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_test_db_config 
engine_test = create_engine(connect_begin)


connect_end= 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_db_config   
engine_formal = create_engine(connect_end)


def transfer_between_db(begin,end,sql):
	table_name=sql.split('`')[1]
	df=pd.read_sql(sql,con=begin)
	df.to_sql(table_name,con=end,if_exists='append',index=False)
	print(table_name+' is ok,please check your data in your database')


def create_new_table(begin,end,sql,table_name):
	df=pd.read_sql(sql,con=begin)
	df.to_sql(table_name,con=end,if_exists='append',index=False)
	print(table_name + 'is ok')

if __name__ =="__main__":
	transfer_between_db(engine_formal,engine_test,sql_doc.sql_member)
	transfer_between_db(engine_formal,engine_test,sql_doc.sql_order)
	transfer_between_db(engine_formal,engine_test,sql_doc.sql_member_cv)
	transfer_between_db(engine_formal,engine_test,sql_doc.sql_member_tree)
	transfer_between_db(engine_formal,engine_test,sql_doc.sql_vip_summary)
	create_new_table(engine_formal,engine_test,sql_doc.sql_vip_summary,'stage_vip_summary')


	print("mysql mission is ok")

