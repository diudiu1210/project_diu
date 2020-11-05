import json
import os
import unittest

from common.db_handler import DBhandler
from common.excel_handler import ExcelHandler
from common.helper import get_mobile
from common.logger_handler import LoggerHandler
from common.requests_handler import RequestHandler
from middleware.helper import save_token, Context, replace_label
from middleware.yaml_handler import YamlHandler,yaml_data
from config.setting import config
from lib import ddt
from decimal import Decimal



@ddt.ddt
class TestInvest(unittest.TestCase):
    # 读取Excel里数据
    excel_handler=ExcelHandler(config.data_path)
    data=excel_handler.total_test("invest")
    logger=LoggerHandler(name=yaml_data["logger"]["name"],
                 level=yaml_data["logger"]["level"],
                 file=yaml_data["logger"]["file"],)

    def setUp(self) -> None:
        # 实例化
        self.req=RequestHandler()
        # 一次操作用的是一个db对象，所以放前置条件当中
        self.db=DBhandler(host=yaml_data["database"]["host"],
                 port=yaml_data["database"]["port"],
                 password=yaml_data["database"]["password"],
                 user=yaml_data["database"]["user"],
                 charset=yaml_data["database"]["charset"],
                 database=yaml_data["database"]["database"])
        # 登录
        # save_token()
        # self.token=Context.token
        # self.member_id=Context.member_id


    def tearDown(self) -> None:
        # 关闭浏览器
        self.req.close_session()
        self.db.close()
    @ddt.data(*data)
    def test_invest(self,test_data):
        # 获取member_id token  loan_id
        member_id=Context().member_id
        token=Context().token
        loan_id=Context().loan_id
        # 从数据库中查找id用户的原可用余额
        sql="select * from member where id=%s;"
        user=self.db.query(sql,args=[member_id])
        before_money=user["leave_amount"]
        # 替换，把Excel里#member_id#  #loan_id# 替换成对应的id
        test_data["json"]=replace_label(test_data["json"])
        print(test_data)


        # if "%amount%" in test_data["json"]:
        #     test_data["json"]=test_data["json"].replace("%amount%",str(before_money+Decimal(100)))
        #
        # if "*amount*" in test_data["json"]:
        #     test_data["json"]=test_data["json"].replace("*amount*",str(before_money+Decimal(100)))
        if "*other_loan_id*" in test_data["json"]:
            oth_loan = self.db.query("select * from loan where id=%s limit 100;", args=[1])
            test_data["json"]=test_data["json"].replace("*other_loan_id*",str(oth_loan))

        headers=json.loads(test_data["headers"])
        headers["Authorization"]=token
        res=self.req.visit(test_data["method"],
                            config.host+test_data["url"],
                            json=json.loads(test_data["json"]),
                            headers=headers)
        print(res)

        try:
            self.assertEqual(test_data["expected"],res["code"])
            #  数据库断言
            if res["code"]==0:
                money=json.loads(test_data["json"])["amount"]
                sql = "select * from member where id=%s;"
                after_user = self.db.query(sql, args=[member_id])
                after_money = after_user["leave_amount"]
                self.assertEqual(before_money - Decimal(money), after_money)


            # 写入Excel 中实际结果
            self.excel_handler.write_cell("invest",config.data_path,test_data["case_id"]+1,9,"用例通过")

        except AssertionError as e:
            # 记录logger
            self.logger.error("测试用例失败".format(e))
            # 手动抛出异常，否则测试用例会自动通过，写入Excel
            self.excel_handler.write_cell("invest",config.data_path,test_data["case_id"]+1,9,"用例失败")
            raise e


