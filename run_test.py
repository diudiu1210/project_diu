#-*- coding:UTF-8 -*-
from lib import HTMLTestRunnerNew
import unittest
import os
from datetime import datetime

# 1.初始化testloader
from config.setting import config

testloader=unittest.TestLoader()
# 查找测试用例，加载  discover（测试用例的路径，想用什么方式运行--默认就是测试用例以test_开头,"demo_*.py"）
suite=testloader.discover(config.case_path)
# print(total_suite)
# 先创建report文件夹，然后再文件夹里创建一个test_result.txt

# 跟据时间生成测试报告，动态获取，有两种方法
ts=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
# ts=str(int(time.time()))
file_name="test_result_{}.html".format(ts)
file_path=os.path.join(config.report_path,file_name)
with open(file_path,"wb") as f:
#     初始化运行器,是以普通文本生成测试报告TextTestRunner(参数是打开的文件)
    runner= HTMLTestRunnerNew.HTMLTestRunner(f, verbosity=2, title="丢丢的excel/ddt测试报告", tester="丢丢")
    # 运行测试用例
    runner.run(suite)


