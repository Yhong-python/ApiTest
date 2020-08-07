#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_payManage.py
@time: 2020/5/25 12:07
@desc::增值服务管理-充值管理
'''
import json
import os
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


@allure.epic('增值服务管理')
@allure.feature("充值管理")
class TestPayManage:
    log = Log().getlog()
    db = DB_config()
    uploadAndDownloadFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'UploadAndDownloadFile')
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    accountChargeData = allData.getTestCaseData(menuName='充值管理', belongs='accountCharge')
    rechargeDetailData = allData.getTestCaseData(menuName='充值管理', belongs='rechargeDetail')
    rdids = [i['IDS'] for i in rechargeDetailData]
    couponChargeData = allData.getTestCaseData(menuName='充值管理', belongs='couponCharge')
    OverDrawTopLimitData = allData.getTestCaseData(menuName='充值管理', belongs='OverDrawTopLimit')
    test = Assertions()

    uploadFixtureData = [{"filepath": os.path.join(uploadAndDownloadFilePath, 'rechargepic.jpg'), "base": ""}]

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session
        self.uploadFixtureData[0]['base'] = self.base

    # @pytest.fixture(scope='class')  #用conftest中的
    # def uploadPic(self):
    #     apiUrl = 'adminApi/mdaMediaResourceInfo/upload'
    #     file = {
    #         'file': ('rechargepic.jpg', open('rechargepic.jpg', 'rb')),
    #         'data': None
    #     }
    #     r = self.base.sendRequest(apiUrl, 'post', files=file)
    #     self.test.assert_code(r.json()['code'], 200)
    #     return r.json()

    @allure.severity("normal")
    @allure.title("可用余额充值")
    @pytest.mark.parametrize("uploadPic", uploadFixtureData, indirect=True)
    @pytest.mark.parametrize("data", accountChargeData)
    def test_accountCharge(self, uploadPic, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['rechargeTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sendData['voucher'] = uploadPic['visitUrl']
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @pytest.fixture(scope='class')
    def getCouponCode(self):
        apiUrl = 'adminApi/tblCoupon/couponDown'
        sendData = {
            'id': 204,  # 这里写死导出为名称为：不删除的优惠券
            'num': 1
        }
        self.log.info('本次使用参数:%s' % sendData)
        try:
            r = self.base.sendRequest(apiUrl, 'get', param=sendData)
            print("接口返回内容：", r.json())
        except json.decoder.JSONDecodeError:
            couponContent = r.content.decode()
            self.log.info('优惠券充值码导出成功:%s' % couponContent)
            print('优惠券充值码导出成功:%s' % couponContent)
            return couponContent
        except Exception as e:
            self.log.exception(e)
            raise
        else:
            self.log.error("导出优惠券接口异常")
            self.test.assert_code(r.json()['code'], 200)

    @allure.severity("normal")
    @allure.title("优惠券余额充值")
    @pytest.mark.parametrize("data", couponChargeData)
    def test_couponCharge(self, getCouponCode, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['voucher'] = getCouponCode
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    # @allure.title() 这里不用title，因为只是参数不一样，所以用ids来区分用例
    @pytest.mark.parametrize("data", rechargeDetailData, ids=rdids)
    def test_rechargeDetail(self, data):
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
    @allure.title("可透资金额修改")
    @pytest.mark.parametrize("data", OverDrawTopLimitData)
    def test_updateOverDrawTopLimit(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
