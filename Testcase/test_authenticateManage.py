#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_authenticateManage.py
@time: 2020/5/26 9:40
@desc:增值服务管理-认证管理
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
@allure.feature("认证管理")
class TestAuthenticateManage:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    selectContChannelConfigData = allData.getTestCaseData(menuName='认证管理', belongs='selectContChannelConfig')
    contChannelConfiginfoData = allData.getTestCaseData(menuName='认证管理', belongs='contChannelConfiginfo')
    test = Assertions()

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @pytest.fixture(scope='class')
    def selectContChannelConfig(self, request):
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
    @allure.title("查询认证服务项目列表")
    @pytest.mark.dependency(name='selectConfigInfo')
    @pytest.mark.parametrize("selectContChannelConfig", selectContChannelConfigData, indirect=True)
    def test_selectContChannelConfig(self, selectContChannelConfig):
        assert selectContChannelConfig[1]

    @allure.severity("normal")
    @allure.title("查询认证信息详情")
    @pytest.mark.dependency(depends=['selectConfigInfo'])
    @pytest.mark.parametrize("selectContChannelConfig", selectContChannelConfigData, indirect=True)
    @pytest.mark.parametrize("data", contChannelConfiginfoData)
    def test_contChannelConfiginfo(self, selectContChannelConfig, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        try:
            channelId = selectContChannelConfig[0]['data'][0]['id']
        except KeyError:
            raise Exception("认证通道id获取失败")
        except Exception as e:
            self.log.exception(e)
            raise
        else:
            sendData['id'] = channelId
            self.log.info('本次使用参数:%s' % sendData)
            r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
            self.log.info('接口返回值:%s' % r.json())
            print('接口返回值:%s' % r.json())
            self.test.verifyExpected(r.json(), expected)
