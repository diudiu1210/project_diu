
# 测试数据是json，在json里如何表示Python中的None，--用null表示
# 字符串转化成Python中的字典,用双引号表示json中key value
import json

# 在写到Excel当中的时候，data是一个字符串，把这个字符串转化成Python中的字典
# data='{"mobile_phone":"13327216490","pwd":None}'
# # 如果用eval，那么会报错，因为Python中的字典没有null这个，不能识别，如果把里面换成None就不是json了
# # b=eval(data)
# # 所以json和字典的转化,loads是把json中字符串转化成字典
# a=json.loads(data)
# print(a)

# # 字典转化成json,用json.dumps()
# data_dict={"name":"diudiu","age":None}
# print(json.dumps(data_dict))

# adata={'json':{'mobile':'##','name':'diu'}}
# # adata[json]=adata[json].replace("##","@@@@")
# print(adata[json])

# a=[3,2,1]
# for i in range(1,4):
#     for j in a:
#         if j>=i:
#             print("&&&",end="/t")

import pymysql
