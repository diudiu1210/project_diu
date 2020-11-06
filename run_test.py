
from lib import HTMLTestRunnerNew
import unittest
import os
from datetime import datetime


from config.setting import config

testloader=unittest.TestLoader()
suite=testloader.discover(config.case_path)

ts=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file_name="test_result_{}.html".format(ts)
file_path=os.path.join(config.report_path,file_name)
with open(file_path,"wb") as f:
    runner= HTMLTestRunnerNew.HTMLTestRunner(f, verbosity=2, title="丢丢的excel/ddt测试报告", tester="丢丢")
    runner.run(suite)


