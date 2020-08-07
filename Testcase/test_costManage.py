#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_costManage.py
@time: 2020/5/25 14:52
@desc:增值服务管理-费用管理
'''
import json
import os
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
@allure.feature("费用管理")
class TestCostManage:
    log = Log().getlog()
    db = DB_config()
    uploadAndDownloadFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'UploadAndDownloadFile')
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    consumeDetailData = allData.getTestCaseData(menuName='费用管理', belongs='consumeDetail')
    downloadConsumeData = allData.getTestCaseData(menuName='费用管理', belongs='downloadConsume')
    downloadRechargeData = allData.getTestCaseData(menuName='费用管理', belongs='downloadRecharge')
    test = Assertions()

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @allure.severity("normal")
    @allure.title("查看详情-消费明细")
    @pytest.mark.parametrize("data", consumeDetailData)
    def test_consumeDetail(self, data):
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
    @allure.title("查看详情-导出消费明细")
    @pytest.mark.parametrize("data", downloadConsumeData)
    def test_downloadConsume(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        self.test.assert_code(r.status_code, 200)
        try:
            self.log.info('接口返回值:%s' % r.json())
            print('接口返回值:%s' % r.json())
        except Exception:
            with open(os.path.join(self.uploadAndDownloadFilePath, '消费明细.xls'), 'wb') as f:
                f.write(r.content)
                print('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, '消费明细.xls')))
                self.log.info('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, '消费明细.xls')))
        else:
            self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查看详情-导出充值明细")
    @pytest.mark.parametrize("data", downloadRechargeData)
    def test_downloadRecharge(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        self.test.assert_code(r.status_code, 200)
        try:
            self.log.info('接口返回值:%s' % r.json())
            print('接口返回值:%s' % r.json())
        except Exception:
            with open(os.path.join(self.uploadAndDownloadFilePath, '充值明细.xls'), 'wb') as f:
                f.write(r.content)
                print('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, '充值明细.xls')))
                self.log.info('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, '充值明细.xls')))
        else:
            self.test.verifyExpected(r.json(), expected)
