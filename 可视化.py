# # from pyecharts import Gauge
# # gauge = Gauge('仪表盘示例')

# # gauge.add('完成率',66.67,angle_range=[180,0],scale_range=[0,100],is_legend_show=False)
# # gauge


# # 自动发帖
# import time
# from selenium import webdriver

# driver = webdriver.Chrome(r'C:\Users\ASUS\Desktop\航运e家\chromedriver_win32\chromedriver.exe')
# xueqiuUrl='https://xueqiu.com/'
# driver.get(xueqiuUrl)
# driver.refresh()         #刷新页面
# # driver.maximize_window() #浏览器最大化
# time.sleep(0.5)

# # 点击登录
# login_box = driver.find_element_by_class_name('Header_nav__login__btn_1YU')
# login_box.click()
# time.sleep(2) # 弹窗出现后，使页面等待2S


# # 获取用户名和密码

# usernameElem=driver.find_element_by_xpath("//input[@name='telephone']")
# usernameElem.send_keys('13761849216')
# time.sleep(0.3)

# login_send_code=driver.find_element_by_class_name('Loginmodal_send-code_3BH')
# login_send_code.click()

# # login_code=driver.find_element_by_class_name('Loginmodal_form-group_17J')
# # code=input("请输入你手机上的验证码:")
# # login_code.send_keys(code)

import requests
def loginEX(session):													 # 登录（手动）
	codeURL = "https://xueqiu.com/account/sms/send_verification_code.json"
	loginURL = "https://xueqiu.com/snowman/login"
	formData = {														 # 登录时使用的表单
		"areacode":"86",
		"remember_me":"true",
		"telephone":"13761849216"
	}		
	codeData = {														 # 获取验证码时提交的表单
		"areacode":"86",
		"telephone":"13761849216",
	}
	session.post(codeURL,codeData)										 # 发送验证码
	formData["code"] = input("请输入验证码：")								 # 获取验证码
	r = session.post(loginURL,formData)	

mainURL = "https://xueqiu.com"
session = requests.Session()
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
session.headers = headers.copy()
session.get(mainURL)
loginEX(session)

