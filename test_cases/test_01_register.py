import json
import os
import unittest

from common.db_handler import DBhandler
from common.excel_handler import ExcelHandler
from common.helper import get_mobile
from common.logger_handler import LoggerHandler
from common.requests_handler import RequestHandler
from middleware.yaml_handler import YamlHandler, yaml_data
from config.setting import config
from lib import ddt


@ddt.ddt
class TestRegister(unittest.TestCase):
    # def setUp(self) -> None:
    # 读取Excel里数据
    excel_handler=ExcelHandler(config.data_path)
    data=excel_handler.total_test("register")
    # 读取yaml里的数据

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
    def test_register(self,test_data):
        print(test_data)
        # 先判断test_data["json"]里如果出现了#exist# 就使用get_mobile随机生成手机号码
        # 查询数据库，如果数据库存在该号码，就使用整个号码，但是整个存在的概率很低，查询不到这个号码，那么Excel中这个用例就有问题
        # 所以先不生成手机号码，先随机从数据库中拿一个已经存在的号码，直接使用该号码替换
        # 然后再用replace替换"#exist#"
        if "#exist#" in test_data["json"]:
            mobile=self.db.query("select * from member limit 1 ;")
            # 判断：如果从数据库中能查到一条记录就替换，如果数据库是空数据库就会执行else
            # 上面的mobile得到的是一个字典，我们需要的是字典里的mobile_phone值
            if mobile:
                # 注意replace替换的一定是一个字符串，如果是数字需要转化
                test_data["json"]=test_data["json"].replace("#exist#",mobile["mobile_phone"])
            else:
                # 随机生成一个 13311112222，如果在库中还是不存在这条用例就会不通过
                # 解决办法：写个注册成功步骤，放到help函数当中，直接调用对应的方法进行注册
                # 先随机生成一个手机号码然后去用request发送注册成功的请求，或者通过db对象往数据库中插入一个手机号码也行，但是不提倡
                pass

        if "#new#" in test_data["json"]:
        # 先判断test_data["json"]里如果出现了#new# 就使用get_mobile随机生成手机号码
        # 查询数据库，如果数据库存在该号码，就再随机生成一个新号码，直到数据库中不存在为止
            while True:
                mobilephone=get_mobile()
                mobile = self.db.query("select * from member where mobile_phone=%s;",args=[mobilephone])
                # 判断：如果随机生成的号码在数据库中就再次循环随机生成一个号码，如果随机生成的号码不在数据库就跳出循环，执行后面的替换语句
                if not mobile:
                    break
            test_data["json"] = test_data["json"].replace("#new#", mobilephone)

        # 访问接口，得到实际结果,res返回的是字典类型，Python里字典，json在Python里是字符串的形式
        res=self.req.visit( test_data["method"],
                            config.host+test_data["url"],
                            json=json.loads(test_data["json"]),
                            headers=json.loads(test_data["headers"]))
        # 获得expected，然后断言
        try:
            self.assertEqual(test_data["expected"],res["code"])
            # 写入Excel 中实际结果
            a=self.excel_handler.write_cell("register",config.data_path,test_data["case_id"]+1,9,"用例通过")
            print(a)

        except AssertionError as e:
            # 记录logger
            self.logger.error("测试用例失败".format(e))
            # 手动抛出异常，否则测试用例会自动通过，写入Excel
            self.excel_handler.write_cell("register",config.data_path,test_data["case_id"]+1,9,"用例失败")
            raise e

        
