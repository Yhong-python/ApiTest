#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_advertiseManage.py
@time: 2020/5/26 11:50
@desc:广告位管理-广告位管理
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


@allure.epic('广告位管理')
@allure.feature("广告位管理")
class TestAdvertiseManage:
    log = Log().getlog()
    db = DB_config()
    uploadAndDownloadFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'UploadAndDownloadFile')
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    selectTblAdData = allData.getTestCaseData(menuName='广告位管理', belongs='selectTblAd')
    insertTbData = allData.getTestCaseData(menuName='广告位管理', belongs='insertTb')
    deleteTbData = allData.getTestCaseData(menuName='广告位管理', belongs='deleteTb')
    test = Assertions()
    # 新增广告位中需要调用一下图片上传接口
    uploadFixtureData = [{"filepath": os.path.join(uploadAndDownloadFilePath, 'advertise.jpeg'), "base": ""}]

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session
        self.uploadFixtureData[0]['base'] = self.base  # 把登录后的session给上传图片接口

    @allure.severity("normal")
    @allure.title("查询广告位列表")
    @pytest.mark.parametrize("data", selectTblAdData)
    def test_selectTblAdPage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        expected = json.loads(data['expected'])
        r = self.base.sendRequest(apiUrl, requestsMethod)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("新增广告位")
    @pytest.mark.dependency(name='addTb')
    @pytest.mark.parametrize("uploadPic", uploadFixtureData, indirect=True)
    @pytest.mark.parametrize("data", insertTbData)
    def test_insertTb(self, uploadPic, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['data']['visitUrl'] = uploadPic['visitUrl']
        sendData['data'] = json.dumps(sendData['data'])
        expected = json.loads(data['expected'])
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("删除广告位")
    @pytest.mark.dependency(depends=['addTb'])
    @pytest.mark.parametrize("data", deleteTbData, indirect=False)  # 参数化时以这种形式
    def test_deleteTb(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        sql = "SELECT id FROM tbl_ad WHERE `name`='接口测试新建广告位'ORDER BY id LIMIT 0,1"
        self.db.excute(sql)
        try:
            id = self.db.get_one()[0]
        except TypeError:
            raise Exception("获取广告位id异常")
        except Exception as e:
            self.log.exception(e)
            raise
        else:
            sendData['id'] = id
            self.log.info('本次使用参数:%s' % sendData)
            r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
            self.log.info('接口返回值:%s' % r.json())
            print('接口返回值:%s' % r.json())
            self.test.verifyExpected(r.json(), expected)
