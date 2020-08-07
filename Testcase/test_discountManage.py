#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_discountManage.py
@time: 2020/5/26 13:53
@desc:优惠券管理-优惠券管理
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


@allure.epic('优惠券管理')
@allure.feature("优惠券管理")
class TestDiscountManage:
    log = Log().getlog()
    db = DB_config()
    uploadAndDownloadFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'UploadAndDownloadFile')
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    tblCouponPageData = allData.getTestCaseData(menuName='优惠券管理', belongs='tblCouponPage')
    addCouponData = allData.getTestCaseData(menuName='优惠券管理', belongs='addCoupon')
    historyPageData = allData.getTestCaseData(menuName='优惠券管理', belongs='historyPage')
    downloadCouponData = allData.getTestCaseData(menuName='优惠券管理', belongs='downloadCoupon')
    deleteCouponData = allData.getTestCaseData(menuName='优惠券管理', belongs='deleteCoupon')
    deleteCouponids = [i['IDS'] for i in deleteCouponData]
    test = Assertions()

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session
        sql = "DELETE FROM tbl_coupon WHERE `name`='接口自动化优惠券'  "  # 数据清理后再执行用例
        self.db.excute(sql)

    @allure.severity("normal")
    @allure.title("查看优惠券列表")
    @pytest.mark.parametrize("data", tblCouponPageData)
    def test_getTblCouponPage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        sendData['search'] = json.dumps({"startDate": "", "endDate": ""})
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("新增优惠券")
    # @pytest.mark.dependency(name='addCoupon')
    @pytest.mark.parametrize("data", addCouponData)
    def test_addTblCoupon(self, data):
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
    @allure.title("查看优惠券详情")
    # @pytest.mark.dependency(depends=['addCoupon'])
    @pytest.mark.parametrize("data", historyPageData)
    def test_historyPage(self, data):
        sql = "SELECT id FROM tbl_coupon  ORDER BY id  DESC LIMIT 0,1"
        self.db.excute(sql)
        try:
            id = self.db.get_one()[0]
        except TypeError:
            raise Exception("获取优惠券id异常")
        except Exception as e:
            self.log.exception(e)
            raise
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        if sendData['couponId'] == '':
            sendData['couponId'] = id
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("导出激活码")
    # @pytest.mark.dependency(depends=['addCoupon'])
    @pytest.mark.parametrize("data", downloadCouponData)
    def test_downloadCoupon(self, data):
        sql = "SELECT id FROM tbl_coupon  ORDER BY id  DESC LIMIT 0,1"
        self.db.excute(sql)
        try:
            id = self.db.get_one()[0]
        except TypeError:
            raise Exception("获取优惠券id异常")
        except Exception as e:
            self.log.exception(e)
            raise
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        if sendData['id'] == '':
            sendData['id'] = id
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        self.test.assert_code(r.status_code, 200)
        try:
            self.log.info('接口返回值:%s' % r.json())
            print('接口返回值:%s' % r.json())
        except json.decoder.JSONDecodeError:
            with open(os.path.join(self.uploadAndDownloadFilePath, '优惠券激活码.xls'), 'wb') as f:
                f.write(r.content)
                print('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, '优惠券激活码.xls')))
                self.log.info('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, '优惠券激活码.xls')))
        except Exception as e:
            self.log.exception(e)
            raise
        else:
            self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    # @allure.title("关闭优惠券")
    # @pytest.mark.dependency(depends=['addCoupon'])
    @pytest.mark.parametrize("data", deleteCouponData, ids=deleteCouponids)
    def test_deleteCoupon(self, data):
        sql = "SELECT id FROM tbl_coupon  ORDER BY id  DESC LIMIT 0,1"
        self.db.excute(sql)
        try:
            id = self.db.get_one()[0]
        except TypeError:
            raise Exception("获取优惠券id异常")
        except Exception as e:
            self.log.exception(e)
            raise
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        if sendData['id'] == '':
            sendData['id'] = id
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
