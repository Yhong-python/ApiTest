#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_visaInterViewRecordManage.py
@time: 2020/5/25 10:08
@desc:远程面签管理-机构面签记录
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


@allure.epic('远程面签管理')
@allure.feature("机构面签记录")
class TestVisaInterviewRecord:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    uploadAndDownloadFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'UploadAndDownloadFile')
    PhoneRecordDate = allData.getTestCaseData(menuName='机构面签记录', belongs='getPhoneRecord')
    downloadPhoneRecordData = allData.getTestCaseData(menuName='机构面签记录', belongs='downloadPhoneRecord')
    test = Assertions()

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @allure.severity("normal")
    @allure.title("查看机构下面签记录列表")
    @pytest.mark.parametrize("data", PhoneRecordDate, indirect=False)  # 参数化时以这种形式
    def test_getRecodList(self, data):
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
    @allure.title("下载面签记录视频")
    @pytest.mark.parametrize("data", downloadPhoneRecordData, indirect=False)  # 参数化时以这种形式
    def test_downloadRecodFile(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        self.test.assert_code(r.status_code, 200)
        try:
            print("接口返回值:{}".format(r.json()))
            self.log.info("接口返回值:{}".format(r.json()))
        except AttributeError:
            with open(os.path.join(self.uploadAndDownloadFilePath, 'video_single.zip'), 'wb') as f:
                f.write(r.content)
                self.test.verifyExpected(r.json(), expected)
                print('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, 'video_single.zip')))
                self.log.info('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, 'video_single.zip')))
        except Exception as e:
            self.log.exception(e)
            raise
        else:
            raise ValueError("下载接口返回值类型不应为dict")
