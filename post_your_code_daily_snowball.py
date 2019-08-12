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
