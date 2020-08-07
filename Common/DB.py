#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: DB.py
@time: 2019/6/5 15:57
@desc:数据库连接封装
'''
import pymysql

from Common.logger import Log
from Conf.Config import Config

cfg = Config()
host = cfg.dbhost
port = cfg.dbport
user = cfg.dbuser
passwd = cfg.dbpwd
dbname = cfg.dbname


# print(host,port,user,passwd,dbname)
# log = Log().getlog()


class DB_config:
    def __init__(self, host=host, port=int(port), user=user, passwd=passwd, db=dbname):
        self.log = Log().getlog()
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def connectDB(self):
        try:
            self.con = pymysql.connect(host=self.host,
                                       port=self.port,
                                       user=self.user,
                                       passwd=self.passwd,
                                       db=self.db,
                                       charset='utf8')
        except Exception as e:
            self.log.error("数据库连接失败%s" % e, exc_info=True)
        self.cur = self.con.cursor()

    def connectDB_otherdb(self, otherdbname):
        try:
            self.con = pymysql.connect(host=self.host,
                                       port=self.port,
                                       user=self.user,
                                       passwd=self.passwd,
                                       db=otherdbname,
                                       charset='gb2312')

        except Exception as e:
            self.log.error("数据库连接失败%s" % e, exc_info=True)
        self.cur = self.con.cursor()

    def excute_otherdb(self, sql, otherdbname):
        self.connectDB_otherdb(otherdbname)  # 连接不同的数据库名称
        try:
            self.cur.execute(sql)
            if 'INSERT' in sql.upper() or 'UPDATE' in sql.upper() or 'DELETE' in sql.upper():
                # print('需要进行commit操作')
                self.con.commit()
            else:
                pass
        except Exception as e:
            print('执行SQL语句失败', e)

    def excute(self, sql):
        self.connectDB()
        try:
            self.cur.execute(sql)
            if 'INSERT' in sql.upper() or 'UPDATE' in sql.upper() or 'DELETE' in sql.upper():
                # self.log.info('需要进行commit操作')
                self.con.commit()
            else:
                pass
        except Exception as e:
            print('执行SQL语句失败', e)

    def get_all(self):
        return self.cur.fetchall()

    def get_one(self):
        return self.cur.fetchone()

    def close(self):
        return self.con.close()


if __name__ == "__main__":
    a = DB_config()
    sql = "SELECT opi.processKey,opi.bankId,pd.id pmsbankid FROM qp_itfin2_data_%d.ovf_process_info opi LEFT JOIN " \
          "qp_itfin2.pms_department pd on opi.bankId=pd.id WHERE processKey = '%s'" % (134, 'chengduyushangjianhang')
    a.excute(sql)
    data = a.get_one()
    print(data)
