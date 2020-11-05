import json
import os
import unittest

from common.db_handler import DBhandler
from common.excel_handler import ExcelHandler
from common.helper import get_mobile
from common.logger_handler import LoggerHandler
from common.requests_handler import RequestHandler
from middleware.yaml_handler import yaml_data
from config.setting import config
from lib import ddt


@ddt.ddt
class TestLogin(unittest.TestCase):
    # def setUp(self) -> None:
    # 读取Excel里数据
    excel_handler=ExcelHandler(config.data_path)
    data=excel_handler.total_test("login")
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

    def tearDown(self) -> None:
        # 关闭浏览器
        self.req.close_session()
        self.db.close()
    @ddt.data(*data)
    def test_login(self,test_data):
        print(test_data)
        # if "#exist#" in test_data["json"]:
        #     # 如果是一个已经存在的手机号码，就直接拿数据库的一个号码，然后登陆成功
        #     mobile=self.db.query("select * from member limit 1;")
        #     print(mobile)
        #     test_data["json"]=test_data["json"].replace("#exist#",mobile["mobile_phone"])
        #     test_data["json"]=test_data["json"].replace("#existpwd#",mobile["pwd"])
        #     print(test_data)

        if "#not exist#" in test_data["json"]:
            while True:
                mobilephone = get_mobile()
                mobile=self.db.query("select * from member where mobile_phone=%s;",args=[mobilephone])
                if not  mobile:
                    break
            test_data["json"]=test_data["json"].replace("#not exist#",mobilephone)

        res=self.req.visit(test_data["method"],
                            config.host+test_data["url"],
                            json=json.loads(test_data["json"]),
                            headers=json.loads(test_data["headers"]))
        print(res)


        # 获得expected，然后断言
        try:
            self.assertEqual(test_data["expected"],res["code"])
            # 写入Excel 中实际结果
            self.excel_handler.write_cell("login",config.data_path,test_data["case_id"]+1,9,"用例通过")
        except AssertionError as e:
            # 记录logger
            self.logger.error("测试用例失败".format(e))
            # 手动抛出异常，否则测试用例会自动通过，写入Excel
            self.excel_handler.write_cell("login",config.data_path,test_data["case_id"]+1,9,"用例失败")
            raise e


