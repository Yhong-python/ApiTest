#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_organizationManage.py
@time: 2020/5/8 10:18
@desc:账号管理-组织机构管理
'''
import json
import time
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
@allure.feature("组织机构管理")
class TestOrganizationManage:
    log = Log().getlog()
    db = DB_config()
    test = Assertions()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    companyListData = allData.getTestCaseData(menuName='组织机构管理', belongs='OrganizationList')
    companyInfoData = allData.getTestCaseData(menuName='组织机构管理', belongs='CompanyInfo')
    UpdateData = allData.getTestCaseData(menuName='组织机构管理', belongs='UpdateCompanyInfo')
    ChangeCompanyStatusData = allData.getTestCaseData(menuName='组织机构管理', belongs='ChangeCompanyStatus')
    adminBankTreeData = allData.getTestCaseData(menuName='组织机构管理', belongs='adminBankTree')

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @allure.severity("normal")  # blocker，critical，normal，minor，trivial 用例级别
    @pytest.mark.parametrize("data", companyListData)
    @allure.title("查看机构列表接口")
    def test_getCompanyList(self, data):
        """获取组织机构数据接口"""
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])  # test_getCompanyList接口的参数
        sendData['search'] = json.dumps({'name': ""})  # search参数需要重新处理一下
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @pytest.fixture(scope='class')
    def companyInfo(self, request):
        apiUrl = request.param['ApiUrl']
        requestsMethod = request.param['Method']
        sendData = json.loads(request.param['Data'])
        expected = json.loads(request.param['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        companyId = sendData['id']
        return r.json(), companyId, self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查看机构详情信息接口")
    @pytest.mark.dependency(name='info')
    @pytest.mark.parametrize("companyInfo", companyInfoData, indirect=True)  # 参数化时以这种形式
    def test_CompanyInfo(self, companyInfo):
        assert companyInfo[2]

    @allure.severity("normal")  # blocker，critical，normal，minor，trivial 用例级别
    @allure.title("修改机构详情接口")
    @pytest.mark.dependency(depends=['info'])
    @pytest.mark.parametrize("companyInfo", companyInfoData, indirect=True)  # 参数化时以这种形式
    def test_updataInfo(self, companyInfo, data=UpdateData[0]):
        '''修改组织信息接口,数据依赖查看组织详情接口'''
        resultData = companyInfo[0]['data']
        apiUrl = data['ApiUrl']
        expected = json.loads(data['expected'])
        requestsMethod = data['Method']
        resultData['idNo'] = '111111111111111111'
        resultData['children'] = []
        resultData.pop('datasourceId')
        resultData.pop('basePartnerId')
        timeStamp = resultData['contractDate'] / 1000
        timeArray = time.localtime(timeStamp)
        resultData['contractDate'] = time.strftime("%Y-%m-%d", timeArray)
        sendData = {
            'data': json.dumps(resultData)
        }
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("修改机构状态接口")
    @pytest.mark.parametrize("data", ChangeCompanyStatusData, indirect=False)  # 参数化时以这种形式
    def test_changeStatus(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        partnerId = sendData['id']
        sql = "SELECT statusFlag FROM qp_itfin2.pms_department WHERE id= %d" % partnerId
        self.db.excute(sql)
        try:
            statusFlag = int(self.db.get_one()[0])
        except Exception as e:
            self.log.info('执行sql获取数据失败')
            self.log.exception(e)
            raise
        self.log.info('机构id:%d当前状态为%d' % (partnerId, statusFlag))
        print('机构id:%d当前状态为%d' % (partnerId, statusFlag))
        if statusFlag == 1:
            self.log.info('当前状态为启用，修改成禁用状态')
            print('当前状态为启用，修改成禁用状态')
            sendData['statusFlag'] = 0
        elif statusFlag == 0:
            self.log.info('当前状态为禁用，修改成启用状态')
            print('当前状态为禁用，修改成启用状态')
            sendData['statusFlag'] = 1
        else:
            raise ValueError('组织机构状态获取错误')
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查看银行列表树接口")
    @pytest.mark.parametrize("data", adminBankTreeData, indirect=False)
    def test_bankList(self, data):
        """查询银行列表树"""
        apiurl = data['ApiUrl']
        requestsMethod = data['Method']
        expected = json.loads(data['expected'])
        r = self.base.sendRequest(apiurl, requestsMethod)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
