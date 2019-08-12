# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 17:18:14 2019
@author: yecheng@cug.edu.cn
"""

import sys
sys.path.append(r"C:\Users\ASUS\Desktop\航运e家\hyej_codestation")
import hyej_db_config

import pymysql
import sqlalchemy
from sqlalchemy import create_engine

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

company_name=[]
tele_phone=[]
contact=[]
company_url=[]

# 建立连接
connect_info='mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8'%hyej_db_config.hyej_test_db_config 
engine = create_engine(connect_info)

driver = webdriver.Chrome(r'C:\Users\ASUS\Desktop\航运e家\chromedriver_win32\chromedriver.exe')
urls=['http://danbao.sol.com.cn/companyList/companyList.asp?pageno=%s' %str(i+1) for i in range(0,8)]

test=[]
for url in urls:
    print(url)
    driver.get(url)


    #获取整个页面信息
    html=driver.page_source
    time.sleep(5)
#    driver.close()
    
    #利用bs解析页面数据
    req=BeautifulSoup(html,'html.parser')
    company_info=req.find('div',class_='company_list').find_all(name='td',class_='companyNameA')
    print(len(company_info))
    for company in company_info:
        company_name.append(company.text.split('|')[0].strip())
        company_url.append(company.find('a')['href'])

    phone_info=req.find('div',class_='company_list').find_all(name='td',align='char')
    print(len(phone_info))
    for phone in phone_info:
        tele_phone.append(phone.text.strip())
        
    contact_info=req.find('div',class_='company_list').find_all(name='td',width="74")
    print(len(contact_info))
    for i in contact_info:
        contact.append(i.text.strip())


driver.close()

contact=[x for x in contact if x!='联系人']

danbao_companyList={
        'company_name':company_name,
        'tele_phone':tele_phone,
        'contact':contact,
        'company_url':company_url}

df=pd.DataFrame(danbao_companyList)


df.to_sql('danbao_companylist',con=engine,if_exists='append',index=False)

print('mission is ok')

