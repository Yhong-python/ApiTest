#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_employeeAcoountManage.py
@time: 2020/5/22 11:50
@desc:账号管理-员工账号管理
'''
import json
import random
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


@allure.epic('账号管理')
@allure.feature("员工账号管理")
class TestEmployeeAccount:
    log = Log().getlog()
    db = DB_config()
    test = Assertions()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    RoleListDate = allData.getTestCaseData(menuName='员工账号管理', belongs='accountList')
    accountDetailData = allData.getTestCaseData(menuName='员工账号管理', belongs='accountDetail')
    addAccountData = allData.getTestCaseData(menuName='员工账号管理', belongs='addAccount')
    updateAccountData = allData.getTestCaseData(menuName='员工账号管理', belongs='updateAccount')
    resetAccountData = allData.getTestCaseData(menuName='员工账号管理', belongs='resetAccount')
    deleteAccountData = allData.getTestCaseData(menuName='员工账号管理', belongs='deleteAccount')
    transferUserListData = allData.getTestCaseData(menuName='员工账号管理', belongs='transferUserList')
    countOrderByUserIdData = allData.getTestCaseData(menuName='员工账号管理', belongs='countOrderByUserId')
    selectAssurerConfigData = allData.getTestCaseData(menuName='员工账号管理', belongs='selectAssurerConfig')
    assureConfigUserListData = allData.getTestCaseData(menuName='员工账号管理', belongs='assureConfigUserList')
    transferOrderData = allData.getTestCaseData(menuName='员工账号管理', belongs='transferOrder')
    getClientRightByUserIdData = allData.getTestCaseData(menuName='员工账号管理', belongs='getClientRightByUserId')
    updateClientRightData = allData.getTestCaseData(menuName='员工账号管理', belongs='updateClientRight')

    fixtureData = []  # 新增角色接口时需要获取角色权限id的前置
    for i in addAccountData:
        fixtureData.append(json.loads(i['ExtraParam']))

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session
        for i in self.fixtureData:
            i['base'] = self.base

    @allure.severity("normal")
    @allure.title("查看机构下员工账号列表接口")
    @pytest.mark.parametrize("data", RoleListDate, indirect=False)  # 参数化时以这种形式
    def test_getDeptUserPage(self, data):
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
    @allure.title("查看员工账号详情接口")
    @pytest.mark.parametrize("data", accountDetailData, indirect=False)  # 参数化时以这种形式
    def test_getUserDetail(self, data):
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
    @allure.title("新建员工账号接口")
    @pytest.mark.dependency(name='addAccount')
    @pytest.mark.parametrize("getNewRoleId", fixtureData, indirect=True)
    @pytest.mark.parametrize("data", addAccountData, indirect=False)  # 参数化时以这种形式
    def test_addNewAccount(self, getNewRoleId, data):
        recidList = getNewRoleId  # 先获取当前机构id下所有的角色权限列表
        if recidList == None:
            self.log.info('当前机构id下没有角色')
            print('当前机构id下没有角色,本次测试无效')
            raise ValueError('当前机构id下没有角色,本次测试无效')
        else:
            apiUrl = data['ApiUrl']
            requestsMethod = data['Method']
            sendData = json.loads(data['Data'])
            sendData['roleId'] = random.choice(recidList)
            expected = json.loads(data['expected'])
            self.log.info('本次使用参数:%s' % sendData)
            r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
            self.log.info('接口返回值:%s' % r.json())
            print('接口返回值:%s' % r.json())
            self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("修改员工账号详情接口")
    @pytest.mark.dependency(depends=['addAccount'])
    @pytest.mark.parametrize("data", updateAccountData, indirect=False)  # 参数化时以这种形式
    def test_updateAccount(self, data):
        sql = "SELECT userId,roleId FROM pms_user WHERE realName='接口自动化测试' AND phone = 13524569871"
        self.db.excute(sql)
        sqldata = self.db.get_one()
        userId, roleId = sqldata[0], sqldata[1]  # 后几个接口都要用到
        if userId == None and roleId == None:
            raise ValueError('获取员工id错误')
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['userId'], sendData['roleId'] = userId, roleId
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("重置员工账号密码接口")
    @pytest.mark.dependency(depends=['addAccount'])
    @pytest.mark.parametrize("data", resetAccountData, indirect=False)  # 参数化时以这种形式
    def test_resetAccount(self, data):
        sql = "SELECT userId FROM pms_user WHERE realName='接口自动化测试' AND phone = 13524569871"
        self.db.excute(sql)
        userId = self.db.get_one()[0]
        if userId == None:
            raise ValueError('获取员工id错误')
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['userId'] = userId
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("删除员工账号接口")
    @pytest.mark.dependency(depends=['addAccount'])
    @pytest.mark.parametrize("data", deleteAccountData, indirect=False)  # 参数化时以这种形式
    def test_deleteAccount(self, data):
        sql = "SELECT userId FROM pms_user WHERE realName='接口自动化测试' AND phone = 13524569871"
        self.db.excute(sql)
        userId = int(self.db.get_one()[0])
        if userId == None:
            raise ValueError('获取员工id错误')
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['userId'] = userId
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查询移交订单接受者列表接口")
    @pytest.mark.parametrize("data", transferUserListData, indirect=False)  # 参数化时以这种形式
    def test_getTransferUserList(self, data):
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
    @allure.title("查询当前账号可移交订单数量统计")
    @pytest.mark.parametrize("data", countOrderByUserIdData, indirect=False)  # 参数化时以这种形式
    def test_countOrderByUserId(self, data):
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
    @allure.title("查询当前账号是否可移交专属业务负责人")
    @pytest.mark.parametrize("data", selectAssurerConfigData, indirect=False)  # 参数化时以这种形式
    def test_getAssurerConfigList(self, data):
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
    @allure.title("查询移交专属业务负责人列表")
    @pytest.mark.parametrize("data", assureConfigUserListData, indirect=False)  # 参数化时以这种形式
    def test_getAssureConfigUserList(self, data):
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
    @allure.title("移交订单以及专属业务负责人")
    @pytest.mark.parametrize("data", transferOrderData, indirect=False)  # 参数化时以这种形式
    def test_transferOrder(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['apiAssurerConfigs'] = json.dumps(sendData['apiAssurerConfigs'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("获取流程中我的客户权限列表")
    @pytest.mark.parametrize("data", getClientRightByUserIdData, indirect=False)  # 参数化时以这种形式
    def test_getClientRightByUserId(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("修改流程中我的客户权限")
    @pytest.mark.parametrize("data", updateClientRightData, indirect=False)  # 参数化时以这种形式
    def test_updataClientRightByProcessId(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        sql = "SELECT id FROM pms_user_client WHERE userId=%d" % sendData['userId']
        self.db.excute(sql)
        try:
            clientId = int(self.db.get_one()[0])
        except TypeError as e:
            self.log.error(e)
        except Exception as e:
            self.log.exception(e)
            raise
        else:
            sendData['clientId'] = clientId
        print(sendData)
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
