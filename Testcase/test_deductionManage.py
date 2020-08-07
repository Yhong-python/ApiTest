#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_deductionManage.py
@time: 2020/5/25 15:53
@desc:增值服务管理-扣款管理
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
@allure.feature("扣款管理")
class TestDeductionManage:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    selectInfoData = allData.getTestCaseData(menuName='扣款管理', belongs='selectInfo')
    getDeductConfigListData = allData.getTestCaseData(menuName='扣款管理', belongs='getDeductConfigList')
    ChannelBankData = allData.getTestCaseData(menuName='扣款管理', belongs='channelBank')
    insertChannelBankData = allData.getTestCaseData(menuName='扣款管理', belongs='insertChannelBank')
    getChannelBankDetailData = allData.getTestCaseData(menuName='扣款管理', belongs='getChannelBankDetail')
    updateChannelBankDetailData = allData.getTestCaseData(menuName='扣款管理', belongs='updateChannelBankDetail')
    changeChannelBankStatusData = allData.getTestCaseData(menuName='扣款管理', belongs='changeChannelBankStatus')
    test = Assertions()

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    def teardown_class(self):
        sql = "DELETE FROM cpt_partner_deduct_channel_config WHERE bankCode = 0104 " \
              "AND directSingleLimit=12345678 AND deductId ={}".format(deductId)  # 数据清理后再执行用例
        self.db.excute(sql)

    @pytest.fixture(scope='class')
    def selectDeductConfigInfo(self, request):
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
    @allure.title("查询扣款渠道信息")
    @pytest.mark.dependency(name='ConfigInfo')
    @pytest.mark.parametrize("selectDeductConfigInfo", selectInfoData, indirect=True)
    def test_selectDeductConfigInfo(self, selectDeductConfigInfo):
        assert selectDeductConfigInfo[1]

    @allure.severity("normal")
    @allure.title("查询扣款渠道银行配置信息")
    @pytest.mark.dependency(depends=['ConfigInfo'])
    @pytest.mark.parametrize("selectDeductConfigInfo", selectInfoData, indirect=True)
    @pytest.mark.parametrize("data", getDeductConfigListData)
    def test_consumeDetail(self, selectDeductConfigInfo, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['deductId'] = selectDeductConfigInfo[0]['data'][0]['id']
        expected = json.loads(data['expected'])
        global deductId
        deductId = sendData['deductId']
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查询扣款渠道银行列表")
    @pytest.mark.dependency(depends=['ConfigInfo'])
    @pytest.mark.parametrize("selectDeductConfigInfo", selectInfoData, indirect=True)
    @pytest.mark.parametrize("data", ChannelBankData)
    def test_getChannelBank(self, selectDeductConfigInfo, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['oldchannelId'] = selectDeductConfigInfo[0]['data'][0]['oldchannelId']
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("新建扣款渠道银行")
    @pytest.mark.dependency(name='addbank', depends=['ConfigInfo'])
    @pytest.mark.parametrize("selectDeductConfigInfo", selectInfoData, indirect=True)
    @pytest.mark.parametrize("data", insertChannelBankData)
    def test_addChannelBank(self, selectDeductConfigInfo, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['deductId'] = selectDeductConfigInfo[0]['data'][0]['id']
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @pytest.fixture(scope='class')
    def getChannelBankDetail(self, request):
        sql = "SELECT id FROM cpt_partner_deduct_channel_config WHERE bankCode = 0104 AND directSingleLimit=12345678 AND deductId ={}".format(
            deductId)
        self.db.excute(sql)
        try:
            id = self.db.get_one()[0]
        except TypeError:
            self.log.error('扣款渠道银行数据获取失败')
            print('扣款渠道银行数据获取失败')
            raise
        except Exception as e:
            self.log.exception(e)
            raise
        apiUrl = request.param['ApiUrl']
        requestsMethod = request.param['Method']
        sendData = json.loads(request.param['Data'])
        sendData['id'] = id
        expected = json.loads(request.param['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        return r.json(), self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查看扣款渠道银行详情")
    @pytest.mark.dependency(name='getBankDetail', depends=['addbank'])
    @pytest.mark.parametrize("getChannelBankDetail", getChannelBankDetailData, indirect=True)
    def test_getChannelBankDetail(self, getChannelBankDetail):
        assert getChannelBankDetail[1]

    @allure.severity("normal")
    @allure.title("修改扣款渠道银行详情")
    @pytest.mark.dependency(depends=['getBankDetail'])
    @pytest.mark.parametrize("getChannelBankDetail", getChannelBankDetailData, indirect=True)
    @pytest.mark.parametrize("data", updateChannelBankDetailData, indirect=False)
    def test_updateChannelBankDetail(self, getChannelBankDetail, data):
        sendData = getChannelBankDetail[0]['data']
        sendData.pop('addTime')
        sendData.pop('bankName')
        sendData.pop('updateTime')
        sendData.pop('status')
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("修改扣款渠道银行状态")
    @pytest.mark.dependency(depends=['addbank'])
    @pytest.mark.parametrize("data", changeChannelBankStatusData, indirect=False)
    def test_changeChannelBankStatus(self, data):
        sql = "SELECT id FROM cpt_partner_deduct_channel_config WHERE bankCode = 0104 AND directSingleLimit=12345678 AND deductId ={}".format(
            deductId)
        self.db.excute(sql)
        try:
            id = self.db.get_one()[0]
        except TypeError:
            self.log.error('扣款渠道银行数据获取失败')
            print('扣款渠道银行数据获取失败')
            raise
        except Exception as e:
            self.log.exception(e)
            raise
        apiUrl = data['ApiUrl']
        sendData = json.loads(data['Data'])
        sendData['id'] = id
        requestsMethod = data['Method']
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
