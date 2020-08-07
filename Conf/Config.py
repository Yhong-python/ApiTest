#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: Config.py
@time: 2020/5/12 11:19
@desc:
'''

import configparser
import os

from Common.logger import Log

log = Log().getlog()


class Config:
    # titles:
    TITLE_ENVIRONMENT = "environment"
    TITLE_TEST = "test"
    TITLE_PRE = "pre"

    # values:
    # [environment]
    VALUE_SWITCH = "switch"

    # values:
    # [test]
    VALUE_ADMINURL = "adminurl"
    VALUE_DBHOST = "dbhost"
    VALUE_DBPORT = "dbport"
    VALUE_DBUSER = "dbuser"
    VALUE_DBPWD = "dbpwd"
    VALUE_DBNAME = "dbname"
    VALUE_ADMINUSER = "adminuser"
    VALUE_ADMINPWD = "adminpwd"
    VALUE_WEBURL = "weburl"
    VALUE_WEBUSER = "webuser"
    VALUE_WEBPWD = "webpwd"

    # path
    path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def __init__(self):
        """
        初始化
        """
        self.config = configparser.RawConfigParser()
        self.log = log
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件config.ini存在！")

        self.config.read(self.conf_path)
        self.environment_switch = self.get_conf(Config.TITLE_ENVIRONMENT, Config.VALUE_SWITCH)
        if self.environment_switch == str(0):
            self.adminurl = self.get_conf(Config.TITLE_TEST, Config.VALUE_ADMINURL)
            self.dbhost = self.get_conf(Config.TITLE_TEST, Config.VALUE_DBHOST)
            self.dbport = self.get_conf(Config.TITLE_TEST, Config.VALUE_DBPORT)
            self.dbuser = self.get_conf(Config.TITLE_TEST, Config.VALUE_DBUSER)
            self.dbpwd = self.get_conf(Config.TITLE_TEST, Config.VALUE_DBPWD)
            self.dbname = self.get_conf(Config.TITLE_TEST, Config.VALUE_DBNAME)
            self.adminuser = self.get_conf(Config.TITLE_TEST, Config.VALUE_ADMINUSER)
            self.adminpwd = self.get_conf(Config.TITLE_TEST, Config.VALUE_ADMINPWD)
            self.weburl = self.get_conf(Config.TITLE_TEST, Config.VALUE_WEBURL)
            self.webuser = self.get_conf(Config.TITLE_TEST, Config.VALUE_WEBUSER)
            self.webpwd = self.get_conf(Config.TITLE_TEST, Config.VALUE_WEBPWD)
            # print(self.adminurl)
            # print(self.dbhost)
            # print(self.dbport)
            # print(self.dbuser)
            # print(self.dbpwd)
            # print(self.dbname)
            # print(self.adminuser)
            # print(self.adminpwd)
            # print(self.weburl)
            # print(self.webuser)
            # print(self.webpwd)
        elif self.environment_switch == str(1):
            self.adminurl = self.get_conf(Config.TITLE_PRE, Config.VALUE_ADMINURL)
            self.dbhost = self.get_conf(Config.TITLE_PRE, Config.VALUE_DBHOST)
            self.dbport = self.get_conf(Config.TITLE_PRE, Config.VALUE_DBPORT)
            self.dbuser = self.get_conf(Config.TITLE_PRE, Config.VALUE_DBUSER)
            self.dbpwd = self.get_conf(Config.TITLE_PRE, Config.VALUE_DBPWD)
            self.dbname = self.get_conf(Config.TITLE_PRE, Config.VALUE_DBNAME)
            self.adminuser = self.get_conf(Config.TITLE_PRE, Config.VALUE_ADMINUSER)
            self.adminpwd = self.get_conf(Config.TITLE_PRE, Config.VALUE_ADMINPWD)
            self.weburl = self.get_conf(Config.TITLE_PRE, Config.VALUE_WEBUSER)
            self.webpwd = self.get_conf(Config.TITLE_PRE, Config.VALUE_WEBPWD)

    def get_conf(self, section, name):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(section, name)

    def set_conf(self, section, name, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(section, name, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, section):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(section)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)


if __name__ == "__main__":
    Config()
    # print(Config().adminurl)
    # Config().set_conf('test','name','123')
    # Config().add_conf('pre')
