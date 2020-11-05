# 这个登录不是测试逻辑，是写我们项目相关的，放到这个中间middle里，不用以test开头
import re

import jsonpath

from common.db_handler import DBhandler
from common.requests_handler import RequestHandler
from config.setting import config
from middleware.yaml_handler import yaml_data

class Context:
    """存放临时数据的地方,context上下文"""

    @property
    def token(self):
        """token 属性，而且属性会动态变化
        Context().token 获取token，自动调用这个方法"""
        data = login()
        t=jsonpath.jsonpath(data,"$..token")[0]
        token_type=jsonpath.jsonpath(data,"$..token_type")[0]
        save_token=" ".join([token_type,t])
        return save_token

    @property
    def member_id(self):
        data=login()
        m=jsonpath.jsonpath(data,"$..id")[0]
        return m
    @property
    def loan_id(self):
        """查询数据库，得到loan_id，临时变量保存到Context
        return 返回loan表中id， loan只会从数据库中查询第一条状态为2的数据"""
        db = DBhandler(host=yaml_data["database"]["host"],
                       port=yaml_data["database"]["port"],
                       password=yaml_data["database"]["password"],
                       user=yaml_data["database"]["user"],
                       charset=yaml_data["database"]["charset"],
                       database=yaml_data["database"]["database"])
        loan=db.query("select * from loan where status=%s limit 100;",args=[2])
        db.close()
        return loan["id"]

def login():
    """登录，返回token 和member_id，访问登陆接口"""
    req=RequestHandler()
    res=req.visit(method="post",
                  url=config.host+"/member/login",
                  json=yaml_data["login"],
                  headers={"X-Lemonban-Media-Type":"lemonban.v2"})
    return res
def save_token():
    """保存token信息"""
    data=login()
    # member_id=data["data"]["id"]
    # token=data["data"]["token_type"]["token"]
    # token_type=data["data"]["token_type"]
    # jsonpath---专门用来解析json路径的工具，jsonpath通过pip install 安装
    # 引入 from jsonpath import jsonpath
    member_id=jsonpath.jsonpath(data,"$..id")[0]
    token=jsonpath.jsonpath(data,"$..token")[0]
    token_type=jsonpath.jsonpath(data,"$..token_type")[0]
    # 第一种方法，直接用return (token,member_id)，用一个元组接收返回值，但是如果数据多的时候就不方便了
    # 第二种方法，直接用一个class Context 类存token和member_id返回值，别的地方需要用到这临时数据时候，直接调用class类即可
    # token 和  token_type进行拼接 用join的时候 里面用一个列表存起来
    token=" ".join([token_type,token])
    # Context.token=token
    # Context.member_id=member_id


def replace_label(target):
    """while循环"""
    re_pattern = r"#(.*?)#"
    while re.findall(re_pattern,target):
    # 如果能够匹配就完成替换
        key=re.search(re_pattern,target).group(1)
        target=re.sub(re_pattern,str(getattr(Context(),key)),target,1)
    return target

if __name__ == '__main__':
    # print(login())
    # data=login()
    print(Context().token)
    print(Context().loan_id)
    print(Context().member_id)
    mystr = '{"member_id":"#member_id#","loan_id":"#loan_id#","token":"#token#"}'
    print(replace_label(mystr))
