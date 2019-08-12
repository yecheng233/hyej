# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 17:32:25 2019

@author: ASUS
"""
import sys
sys.path.append(r"C:\Users\ASUS\Desktop\航运e家\hyej_codestation")
import hyej_db_config
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine



df=pd.read_excel(r'C:\Users\ASUS\Desktop\刷量\8.11航运411.xlsx')
df_new=df[['date','手机号码']]
df_new=df_new.rename(columns={'手机号码':'mobile'})
# 建立连接
connect_info='mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_test_db_config   
engine = create_engine(connect_info)

df_new.to_sql('block_list',con=engine,if_exists='append',index=False)
print("ok")
