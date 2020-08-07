#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: Login.py
@time: 2020/5/11 10:33
@desc: 前后台的登录封装
'''
from Common.base import Base
from Conf.Config import Config


def loginAdmin(usr=None, pwd=None):
    """
    后台登录
    :param usr:
    :param pwd:
    :return: 返回登录后的session
    """
    base = Base()
    base.server_ip = Config().adminurl
    login_api = 'adminApi/admin/sys/login'
    if usr == None and pwd == None:
        usr, pwd = Config().adminuser, Config().adminpwd
    else:
        usr, pwd = usr, pwd
    login_data = {'username': usr,
                  'password': pwd,
                  'captcha': '1111'}
    # print("本次测试登录账号信息为%s,%s" % (usr, pwd))
    try:
        r = base.sendRequest(login_api, 'POST', data=login_data)
        # print(r.json())
        assert r.json()['code'] == 200, '后台登录失败'
    except Exception as e:
        raise
    return base


def loginWeb(usr=None, pwd=None):
    """
    前台登录
    :param usr:
    :param pwd:
    :return: 返回登录后的session
    """
    base = Base()
    base.server_ip = Config().weburl
    login_api = 'wwwApi/admin/sys/login'
    if usr == None and pwd == None:
        usr, pwd = Config().webuser, Config().webpwd
    else:
        usr, pwd = usr, pwd
    login_data = {'username': usr,
                  'password': pwd,
                  'captcha': '1111'}
    cookies = {'userName': '',
               'userPwd': '',
               'JSESSIONID': '',
               'userSessionId': ''}
    print("本次测试登录账号信息为%s,%s" % (usr, pwd))
    try:
        r = base.sendRequest(login_api, 'POST', data=login_data, cookies=cookies)
        print(r.json())
        assert r.json()['code'] == 200, '前台登录失败'
    except Exception as e:
        raise
    return base
