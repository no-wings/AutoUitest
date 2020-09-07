# coding=utf-8
import MySQLdb
import readconfig

localreadconfig = readconfig.ReadConfig()


# class Show_Error(Exception):
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         print('平台上展示的数据不存在于筛选数据中，打印异常数据')


class DbManipulate:
    def __init__(self):
        self.ip = localreadconfig.get_db('ip')
        self.db_username = localreadconfig.get_db('db_username')
        self.db_password = localreadconfig.get_db('db_password')
        self.test_db = localreadconfig.get_db('test_db')
        self.db = MySQLdb.connect(self.ip, self.db_username, self.db_password, self.test_db, charset='utf8')
        self.cursor = self.db.cursor()

    # 语句查询
    def query(self, query_sentence):
        self.cursor.execute(query_sentence)
        result = self.cursor.fetchall()
        return result

    # 查询后再获取字段值
    def get_fields(self):
        fields = self.cursor.description
        return fields