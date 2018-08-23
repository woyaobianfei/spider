# -*- coding:utf-8 -*-

# 导入pymysql模块
import pymysql


class mysql:
    # 初始化函数，初始化连接列表
    def __init__(self):
        self.host = 'xxx.xxx.225.189'
        self.user = 'root'
        self.pwd = 'xxx'
        self.port = xx06
        self.dbname = 'xxx'

    # 获取数据库游标对象cursor
    # 游标对象：用于执行查询和获取结果
    def getCursor(self):

        # 建立数据库连接
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.dbname, port=self.port, use_unicode=True, charset="utf8")

        # 创建游标对象
        cur = self.db.cursor()

        # 返回
        return cur

    # 查询操作
    def queryOperation(self, sql):

        # 建立连接获取游标对象
        cur = self.getCursor()

        # 执行SQL语句
        cur.execute(sql)

        # 获取数据的行数
        row = cur.rowcount

        # 获取查询数据
        # fetch*
        # all 所有数据,one 取结果的一行，many(size),去size行
        dataList = cur.fetchall()

        # 关闭游标对象
        cur.close()

        # 关闭连接
        self.db.close()

        # 返回查询的数据
        return dataList

    # 删除操作
    def deleteOperation(self, sql):

        # 获取游标对象
        cur = self.getCursor()
        try:
            # 执行SQL语句
            cur.execute(sql)

            # 正常结束事务
            self.db.commit()

        except Exception as e:
            print(e)

            # 数据库回滚
            self.db.rollback()

        # 关闭游标对象
        cur.close()

        # 关闭数据库连接
        self.db.close()

    # 数据更新
    def updateOperation(self, sql):
        cur = self.getCursor()
        try:
            cur.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

        cur.close()
        self.db.close()

    # 添加数据
    def insertOperation(self, sql):

        cur = self.getCursor()
        try:
            cur.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

        cur.close()
        self.db.close()