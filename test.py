# from PIL import Image, ImageEnhance
# import os
# # def baiduduqu(filename):
# # 	from aip import AipOcr
# # 	import re
# # 	# import os
# # 	APP_ID = '16819623'
# # 	API_KEY = 'eXRUHtSfqqqsdjohhj3x7VRV'
# # 	SECRET_KEY = 'p4YDFB09rU9PmG5T8ooXjoWNP5wTOiQc'
# # 	client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# # 	dakai = open(filename,'rb')
# # 	duqu = dakai.read()
# # 	message = client.basicGeneral(duqu)
# # 	for duqu in message.get('words_result'):
# # 		print(duqu.get('words'))







# # def filename (fielsoure,filetype):
# # 	import os
# # 	pathDir = os.listdir(filesoure)
# # 	for allDir in pathDir:
# # 		child = os.path.join('%s%s' % (filesoure,allDir))
# # 		print(child)
# # 		baiduduqu(filesoure,child)

 
# if __name__ == '__main__':
# 	# filename= 'C:\\Users\\ASUS\\Desktop\\测试\\左.jpg'

# 	# image = Image.open(filename)
# 	# # 先旋转调整，向左旋转90°,默认是逆时针旋转的度数
# 	# # 设置expand参数为True,放大图像的尺寸以适应整个旋转后的新图像
# 	# f=image.rotate(90,expand=True)
# 	# height,width=f.size

# 	# box=(0,0,height/2,width)
# 	# f.crop(box).save('test.jpg')
# 	# duqu = dakai.read()

# 	filename=r'C:\Users\ASUS\Desktop\航运e家\hyej_codestation\test.jpg'
# 	# text=baiduduqu(filename)
# 	# for i in text:
# 	# 	print(i)
# 	# name=text.split('Full name of the holder')[0].split("持证人姓名")[1]
# 	# print(name)
# 	from aip import AipOcr
# 	import re
# 	# import os
# 	APP_ID = '16819623'
# 	API_KEY = 'eXRUHtSfqqqsdjohhj3x7VRV'
# 	SECRET_KEY = 'p4YDFB09rU9PmG5T8ooXjoWNP5wTOiQc'
# 	client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# 	dakai = open(filename,'rb')
# 	duqu = dakai.read()
# 	# 返回一个dict，结果数据在['words_result']里
# 	message = client.basicGeneral(duqu)
# 	s=[]
# 	for i in message['words_result']:
# 		s.append(i['words'])
# 	strc="".join(s)
# 	print(strc)
# 	name=strc.split('持证人姓名:')[1].split("Full")[0]
# 	print(name)



# # 可视化
# import matplotlib.pyplot as plt 
# squares=[1,4,9,16,25]

# x=[1,2,3,4,5]
# plt.plot(x,squares,linewidth=5)


# # 设置图标标题，并给坐标轴加上标签
# plt.title('Square Numbers',fontsize=24)
# plt.xlabel('Value',fontsize=14)
# plt.ylabel('Square of Value',fontsize=14)

# # 设置刻度标记的大小
# plt.tick_params(axis='both',labelsize=14)
# plt.show()

# from pyecharts import Map
# value = [155, 10, 66, 78, 33, 80, 190, 53, 49.6]
# attr = [
#     "福建", "山东", "北京", "上海", "甘肃", "新疆", "河南", "广西", "西藏"
#     ]
# map = Map("Map 结合 VisualMap 示例", width=1200, height=600)
# map.add(
#     "",
#     attr,
#     value,
#     maptype="china",
#     is_visualmap=True,
#     visual_text_color="#000",
# )
# map.render()



from pyecharts.charts import Bar

bar = Bar()
bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# 也可以传入路径参数，如 bar.render("mycharts.html")
bar.render()
