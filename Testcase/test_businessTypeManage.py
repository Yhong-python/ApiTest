#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_businessTypeManage.py
@time: 2020/5/27 10:28
@desc:业务类型管理-业务类型管理
'''
import json
import warnings

import allure
import pytest

from Common.Assert import Assertions
from Common.DB import DB_config
from Common.Login import loginAdmin
from Common.logger import Log
from Conf.Config import Config
from Params.param import GetData

warnings.simplefilter("ignore", ResourceWarning)


@allure.epic('业务类型管理')
@allure.feature("业务类型管理")
class TestBusinessTypeManage:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    odrProductTypePageDate = allData.getTestCaseData(menuName='业务类型管理', belongs='odrProductTypePage')
    odrProductFromFindListData = allData.getTestCaseData(menuName='业务类型管理', belongs='odrProductFromFindList')
    test = Assertions()

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @allure.severity("normal")
    @allure.title("查询业务类型列表")
    @pytest.mark.parametrize("data", odrProductTypePageDate)
    def test_odrProductTypePage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查询业务来源方列表")
    @pytest.mark.parametrize("data", odrProductFromFindListData)
    def test_odrProductFromFindList(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        expected = json.loads(data['expected'])
        r = self.base.sendRequest(apiUrl, requestsMethod)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)


@allure.epic('业务类型管理')
@allure.feature("业务类型分配")
class TestBusinessTypeAllot:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    test = Assertions()
    BusinessTypeSettingsPageDate = allData.getTestCaseData(menuName='业务类型分配', belongs='BusinessTypeSettingsPage')
    updateEnableFlagData = allData.getTestCaseData(menuName='业务类型分配', belongs='updateEnableFlag')
    enableFlagids = [i['IDS'] for i in updateEnableFlagData]

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @allure.severity("normal")
    @allure.title("机构业务类型列表")
    @pytest.mark.parametrize("data", BusinessTypeSettingsPageDate)
    def test_BusinessTypeSettingsPage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @pytest.mark.parametrize("data", updateEnableFlagData, ids=enableFlagids)
    def test_updateEnableFlag(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
