import os
class Config():
    # 项目路径
    root_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # data数据路径
    data_path=os.path.join(root_path,"data/case.xlsx")

    # 测试用例路径
    case_path=os.path.join(root_path,"test_cases")
    # 测试报告的路径
    report_path = os.path.join(root_path, "report")
    if not os.path.exists(report_path):
        os.mkdir(report_path)        
    # 配置config文件夹的路径
    config_path=os.path.join(root_path,"config")   
    # config配置里yaml的路径
    yaml_config_path=os.path.join(config_path,"config.yaml")
    
    
class Devconfig(Config):
    # 项目的域名
    host="http://120.78.128.25:8766/futureloan"

config=Devconfig()