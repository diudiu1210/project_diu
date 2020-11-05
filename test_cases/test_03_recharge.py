import json
import os
import unittest

from common.db_handler import DBhandler
from common.excel_handler import ExcelHandler
from common.helper import get_mobile
from common.logger_handler import LoggerHandler
from common.requests_handler import RequestHandler
from middleware.helper import save_token, Context
from middleware.yaml_handler import YamlHandler,yaml_data
from config.setting import config
from lib import ddt
from decimal import Decimal



@ddt.ddt
class TestRecharge(unittest.TestCase):
    # def setUp(self) -> None:
    # 读取Excel里数据
    excel_handler=ExcelHandler(config.data_path)
    data=excel_handler.total_test("recharge")
    # 读取yaml里的数据
    # yaml_data =YamlHandler(config.yaml_config_path).yaml_read()
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
    def test_recharge(self,test_data):
        """充值接口
        1、替换json数据当中member_id
        2、访问接口，得到实际结果
        3、断言实际结果，同时需要查数据库里面充值金额是否正确"""
        # 进行充值时候member_id是动态变化的，amount是规定好的可以写死，headers里需要用登陆时候返回的token：
        # 处理token第一种：在Excel里的headers里，用## 动态生成，然后用replace替换；第二种是在前置条件登陆中拿到token，然后再发送requests请求中的headers上拼接上token
        # 充值之前，查询数据库，获取充值之前的余额
        member_id=Context().member_id
        token=Context().token

        sql="select * from member where id=%s;"
        user=self.db.query(sql,args=[member_id])
        before_money=user["leave_amount"]

        if "#member_id#" in test_data["json"]:
            test_data["json"]=test_data["json"].replace("#member_id#",str(member_id))
        # 错误的用户名用例，只要不要等于当前登录的id就行，可以id+1 +2 都行
        if "#other_id#" in test_data["json"]:
            test_data["json"]=test_data["json"].replace("#other_id#",str(member_id+1))
        # 读取Excel中headers，这个得到的是字典
        headers=json.loads(test_data["headers"])
        # 得到Authorization信息头
        headers["Authorization"]=token
        res=self.req.visit(test_data["method"],
                            config.host+test_data["url"],
                            json=json.loads(test_data["json"]),
                            headers=headers)
        print(res)


        # 获得expected，然后断言
        try:
            self.assertEqual(test_data["expected"],res["code"])
            # 第二次断言，充值成功的用例需要进行数据库校验，金额
            # 判断是否为成功用例，通过返回码判断，如果没有code可以用msg 或者在Excel新增一列tag ，success
            if res["code"]==0:
                # 查看数据库结果，充值之前的金额+ 充值的金额=充值后的金额
                money=json.loads(test_data["json"])["amount"]
                # 获取充值之前的金额：第一种办法是通过save_token返回的leave_amount,这个方法如果是多次充值的时候，会获取失败，为此应该把save_token()放前置条件中，保证每次用例之前都获取一次

                sql = "select * from member where id=%s;"
                after_user = self.db.query(sql, args=[member_id])
                after_money = after_user["leave_amount"]
                self.assertEqual( before_money + Decimal(money) , after_money)

            # 写入Excel 中实际结果
            self.excel_handler.write_cell("recharge",config.data_path,test_data["case_id"]+1,9,"用例通过")
        except AssertionError as e:
            # 记录logger
            self.logger.error("测试用例失败".format(e))
            # 手动抛出异常，否则测试用例会自动通过，写入Excel
            self.excel_handler.write_cell("recharge",config.data_path,test_data["case_id"]+1,9,"用例失败")
            raise e



