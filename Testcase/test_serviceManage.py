#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_serviceManage.py
@time: 2020/5/25 11:19
@desc:增值服务管理-服务项管理
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


@allure.epic('增值服务管理')
@allure.feature("服务项管理")
class TestServiceManage:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    test = Assertions()
    accountInfoDate = allData.getTestCaseData(menuName='服务项管理', belongs='accountInfo')
    accountDetailDate = allData.getTestCaseData(menuName='服务项管理', belongs='accountDetail')
    accountSaveDate = allData.getTestCaseData(menuName='服务项管理', belongs='accountSave')

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @allure.severity("normal")
    @allure.title("查询机构的服务项目账户余额")
    @pytest.mark.parametrize("data", accountInfoDate)
    def test_accountInfo(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @pytest.fixture(scope='class')
    def accountDetail(self, request):
        apiUrl = request.param['ApiUrl']
        requestsMethod = request.param['Method']
        sendData = json.loads(request.param['Data'])
        expected = json.loads(request.param['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        return r.json(), self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查询机构的服务项目详情")
    @pytest.mark.dependency(name='detail')
    @pytest.mark.parametrize("accountDetail", accountDetailDate, indirect=True)
    def test_accountDetail(self, accountDetail):
        assert accountDetail[1]

    @allure.severity("normal")
    @allure.title("服务项目保存接口")
    # @pytest.mark.dependency(depends=["detail"])  # 用例依赖上一接口，若上一接口执行失败直接跳过。用例依赖间又需要获取前面的返回值
    @pytest.mark.parametrize("accountDetail", accountDetailDate, indirect=True)
    @pytest.mark.parametrize("data", accountSaveDate, indirect=False)
    def test_serviceUpdata(self, accountDetail, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['accountDetail'] = json.dumps(accountDetail[0]['data'])  # 直接保存，不修改数据
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
