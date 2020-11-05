# logging模块里有个logger类，里面包括debug等方法，直接继承logging.Logger
import logging

class LoggerHandler(logging.Logger):
    def __init__(self,
                 name="root",
                 level="DEBUG",
                 file=None,
                 format="%(name)s-%(filename)s-%(levelname)s-%(lineno)s-%(message)s"):
        super().__init__(name)
        self.setLevel(level)
        # 如果file为空的话就会执行默认StreamHandler打印到控制台，如果有file，就会两个都执行。
        if file:
            handler=logging.FileHandler(file)
            handler.setLevel(level)
            self.addHandler(handler)
            fmt=logging.Formatter(format)
            handler.setFormatter(fmt)
        console_handler=logging.StreamHandler()
        console_handler.setLevel(level)
        self.addHandler(console_handler)
        fmt=logging.Formatter(format)
        console_handler.setFormatter(fmt)
# 小技巧：可以在定义的模块中初始化
# logger=LoggerHandler("pyth25","python25_log.txt")
# 
# if __name__ == '__main__':
#     logger=LoggerHandler(file="log1.txt")
#     logger.debug("helloword")

