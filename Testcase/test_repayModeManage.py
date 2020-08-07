#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_repayModeManage.py
@time: 2020/6/8 11:49
@desc:还款方式管理
'''
import warnings

import allure
import pytest

from Common.Assert import Assertions
from Common.DB import DB_config
from Common.Login import loginAdmin
from Common.logger import Log
from Common.operateYamlAndJson import *
from Conf.Config import Config
from Params.param import GetData

warnings.simplefilter("ignore", ResourceWarning)


@allure.epic('还款方式管理')
class TestRepayModeManage:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    getRepayMethodListData = allData.getTestCaseData(menuName='还款方式管理', belongs='getRepayMethodList')
    inOrUpRepayModeData = allData.getTestCaseData(menuName='还款方式管理', belongs='inOrUpRepayMode')
    inOrUpRepayModeIds = [i['IDS'] for i in inOrUpRepayModeData]
    infoData = allData.getTestCaseData(menuName='还款方式管理', belongs='info')
    infoIds = [i['IDS'] for i in infoData]
    enableOrProhibitData = allData.getTestCaseData(menuName='还款方式管理', belongs='enableOrProhibit')
    enableOrProhibitIds = [i['IDS'] for i in enableOrProhibitData]
    test = Assertions()
    # 接口返回值sql校验文件路径
    yamlfilepath = os.path.join((os.path.dirname(os.path.dirname(__file__))), 'VerifyJsonAndSql',
                                'repayModeManage.yaml')
    jsonfilepath = os.path.join((os.path.dirname(os.path.dirname(__file__))), 'VerifyJsonAndSql',
                                'repayModeManage.json')

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session
        # 删除添加的“自动化新增-按日计息”还款方式
        delteAlreadyExistSql = readYaml(self.yamlfilepath)['data']['setupsql']['delteAlreadyExistSql']
        self.db.excute(delteAlreadyExistSql)

        # 修改id=10的还款方式字段值到初始值
        resetStartSQL = readYaml(self.yamlfilepath)['data']['setupsql']['resetStartSQL']
        self.db.excute(resetStartSQL)

    @allure.severity("normal")
    @allure.title("查询还款方式列表")
    @pytest.mark.parametrize("data", getRepayMethodListData)
    def test_getRepayMethodList(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        if r.json()['code'] == 200:  # 状态码200时再进行数据校验
            verifyJson = getApiJsonData(self.jsonfilepath, 'getRepayMethodList')
            assert r.json() == verifyJson

    @allure.severity("normal")
    @allure.title("新建还款方式")
    @pytest.mark.parametrize("data", inOrUpRepayModeData, ids=inOrUpRepayModeIds)
    def test_inOrUpRepayMode(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库字段值校验
        if r.json()['code'] == 200:
            if sendData['id'] == '':  # 执行新增的数据校验
                verifySql = readYaml(self.yamlfilepath)['data']['inOrUpRepayMode']['verifySql']
                self.db.excute(verifySql)
                dbresult = self.db.get_one()
                assert sendData['partnerId'] == dbresult[1], "接口传参与数据库实际值不匹配"
                assert sendData['name'] == dbresult[2], "接口传参与数据库实际值不匹配"
                assert sendData['calculateType'] == dbresult[3], "接口传参与数据库实际值不匹配"
                assert sendData['partnerId'] == dbresult[1], "接口传参与数据库实际值不匹配"
                for i in range(12)[4:]:
                    assert dbresult[i] == ''
                assert sendData['allDayFormula'] == dbresult[13], "接口传参与数据库实际值不匹配"
                assert sendData['principalDayFormula'] == dbresult[14], "接口传参与数据库实际值不匹配"
                assert sendData['interestDayFormula'] == dbresult[15], "接口传参与数据库实际值不匹配"
            else:  # 执行修改的校验
                updateSql = readYaml(self.yamlfilepath)['data']['inOrUpRepayMode']['updateSql']
                self.db.excute(updateSql)
                dbresult = self.db.get_one()
                assert sendData['partnerId'] == dbresult[1], "接口传参与数据库实际值不匹配"
                assert sendData['name'] == dbresult[2], "接口传参与数据库实际值不匹配"
                assert sendData['calculateType'] == dbresult[3], "接口传参与数据库实际值不匹配"
                assert sendData['partnerId'] == dbresult[1], "接口传参与数据库实际值不匹配"
                for i in range(12)[4:]:
                    assert dbresult[i] == ''
                assert sendData['allDayFormula'] == dbresult[13], "接口传参与数据库实际值不匹配"
                assert sendData['principalDayFormula'] == dbresult[14], "接口传参与数据库实际值不匹配"
                assert sendData['interestDayFormula'] == dbresult[15], "接口传参与数据库实际值不匹配"

    @allure.severity("normal")
    # @allure.title("查询还款方式详情")
    @pytest.mark.parametrize("data", infoData, ids=infoIds)
    def test_info(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        if r.json()['code'] == 200:  # 状态码200时再进行数据校验
            if sendData['id'] == 1:
                verifyJson = getApiJsonData(self.jsonfilepath, 'info')
                assert r.json() == verifyJson
            elif sendData['id'] == 2:
                verifyJson = getApiJsonData(self.jsonfilepath, 'info2')
                assert r.json() == verifyJson
            else:
                raise ValueError('sendData中的id与预期数据不匹配')

    @allure.severity("normal")
    # @allure.title("启用/禁用还款方式")
    @pytest.mark.parametrize("data", enableOrProhibitData, ids=enableOrProhibitIds)
    def test_enableOrProhibit(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库字段值校验
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['enableOrProhibit']['verifySql']
            self.db.excute(verifySql)
            dbresult = self.db.get_one()
            assert sendData['status'] == dbresult[0], "接口传参与数据库实际值不匹配"
