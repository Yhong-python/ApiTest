#!/usr/bin/env python
# encoding: utf-8
#
'''
@author: yanghong
@file: conftest.py
@time: 2020/5/11 12:04
@desc:
'''
import os

import pytest

from Common.base import Base
from Common.logger import Log
from Conf.Config import Config

log = Log().getlog()


# 上一用例失败，下一用例跳过。在用例中的使用方法，上一个用例失败或跳过getattr(Falied,testcasename,False)==True时,跳过
# @pytest.mark.skipif(getattr(Falied, 'test1', False)==True,reason='test1 执行失败或被跳过，此用例跳过！')
class Falied:
    skip = False


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport():
    result = yield
    report = result.get_result()
    # 当前用例名
    case_name = report.nodeid.split('::')[-1]
    # 当某个用例失败时(setup失败也算)或被跳过时，将这个用例的执行结果存储在 Failed 类中
    if report.when in ('setup', 'call') and report.outcome in ('failed', 'skipped'):
        setattr(Falied, case_name, True)


@pytest.fixture(scope='class', autouse=False)
def loginAdmin(request):
    base = Base()
    base.server_ip = Config().adminurl
    login_api = 'adminApi/admin/sys/login'
    usr = Config().adminuser
    pwd = Config().adminpwd
    try:
        usr = request.param['user']
        pwd = request.param['pwd']
    except AttributeError as e:
        print('本次测试未指定后台账号,默认登录账号为%s' % usr)

    login_data = {'username': usr,
                  'password': pwd,
                  'captcha': '1111'}
    print("本次登录账号信息为%s,%s" % (usr, pwd))
    try:
        r = base.sendRequest(login_api, 'POST', data=login_data)
        assert r.json()['code'] == 200, '后台登录失败，本次测试无效'
    except Exception:
        raise
    return base


@pytest.fixture(scope='class')
def getNewRoleId(request):
    apiUrl = 'adminApi/pmsRole/list'
    sendData = {
        "departmentId": request.param['departmentId']
    }
    r = request.param['base'].sendRequest(apiUrl, 'post', param=sendData)
    recidList = [i['recid'] for i in r.json()['data']]  # 列表生成式,获取角色ID
    return recidList


@pytest.fixture(scope='function')
def uploadPic(request):
    apiUrl = 'adminApi/mdaMediaResourceInfo/upload'
    file = {
        'file': (request.param['filepath'], open(request.param['filepath'], 'rb')),
        'data': None
    }
    r = request.param['base'].sendRequest(apiUrl, 'post', files=file)
    return r.json()


@pytest.fixture(scope='session', autouse=True)
def deleteFile():
    # 执行用例之前，删除UploadAndDownloadFile文件夹下的四个文件：省市区下载.xls/充值明细.xls/消费明细.xls/优惠券激活码.xls
    uploadAndDownloadFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'UploadAndDownloadFile')
    for fileName in os.listdir(uploadAndDownloadFilePath):
        if fileName == '省市区下载.xls' or fileName == '充值明细.xls' or fileName == '消费明细.xls' or fileName == '优惠券激活码.xls':
            os.remove(os.path.join(uploadAndDownloadFilePath, fileName))
    yield
