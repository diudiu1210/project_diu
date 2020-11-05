import pymysql
from pymysql.cursors import DictCursor
from middleware.yaml_handler import YamlHandler,yaml_data
from config.setting import config


class DBhandler():
    def __init__(self,host, port,password, user,charset, database,cursorclass=DictCursor,**kw):
        """初始化，把conn放实例属性里，下面关闭连接的时候可以直接用self调用"""
        self.conn = pymysql.connect(host=host, port=port,
                               password=password, user=user,
                               charset=charset, database=database, cursorclass=DictCursor,**kw)
        self.cursor=self.conn.cursor()
    def query(self,sql,args=None,one=True):
        """ 查询语句"""
        self.cursor.execute(sql,args)
        # TODO:提交事务。数据同步，保证每次去数据库查的数据都是最新的
        self.conn.commit()
        # 如果one是Ture 就用fetchone  如果参数传递是one=False就是fetchall
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()
        
    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    yaml_data = YamlHandler(config.yaml_config_path).yaml_read()
    print(yaml_data)
    db=DBhandler(host=yaml_data["database"]["host"],
                 port=yaml_data["database"]["port"],
                 password=yaml_data["database"]["password"],
                 user=yaml_data["database"]["user"],
                 charset=yaml_data["database"]["charset"],
                 database=yaml_data["database"]["database"])
    res=db.query("select * from member limit 2;")
    print(res)


