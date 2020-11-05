import requests
class RequestHandler():
    def __init__(self):
        self.session=requests.Session()

    # 方法一，直接通过requests里有request的方法直接调用就行
    # def visit1(self,method,url,**kwargs):
    #     res = requests.request(method,url,**kwargs)
    #     return res.json()
    # 方法二，通过session里request方法里，调用，json是必须传的参数，要不然报错
    def visit(self,method,url,data=None,params=None,json=None,**kwargs):
        res=self.session.request(method,url,json=json,**kwargs)
        try:
            return res.json()
        except ValueError:
            print("不是json")

    def close_session(self):
        self.session.close()

