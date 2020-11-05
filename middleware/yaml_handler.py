# 完成 yaml 类的封装，读取yaml 文件和写入 yaml 文件
import yaml

from config.setting import config


class YamlHandler():
    def __init__(self,file,data=None):
        self.file=file
        self.data=data
        self.encoding = "utf-8"

    def yaml_read(self):
        with open(self.file,encoding=self.encoding) as f:
            return yaml.load(f.read(),Loader=yaml.FullLoader)

    def yaml_write(self,):
        with open(self.file,mode="w",encoding=self.encoding) as f:
            yaml.dump(self.data,f,allow_unicode=True)
            
# data=YamlHandler("python25.yaml").yaml_read()
# YamlHandler("python26.yaml",data=data).yaml_write()
# yaml_data获取的是整个项目中yaml配置项里的数据，但是db和requests方法不适合
# 每次需要打开然后关闭DB对象，新的db对象，如果放类里面，每次调用的都是同一个db对象
yaml_data=YamlHandler(config.yaml_config_path).yaml_read()

