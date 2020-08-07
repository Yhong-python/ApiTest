#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_noticeModule.py
@time: 2020/5/27 12:13
@desc:通知管理-常用通知模板
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


@allure.epic('通知管理')
@allure.feature("常用通知模板")
class TestNoticeModule:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    noticeTemplatePageDate = allData.getTestCaseData(menuName='常用通知模板', belongs='noticeTemplatePage')
    addMouldData = allData.getTestCaseData(menuName='常用通知模板', belongs='addMould')
    addMouldIds = [i['IDS'] for i in addMouldData]
    selectNoticeTemplateData = allData.getTestCaseData(menuName='常用通知模板', belongs='selectNoticeTemplate')
    updateNoticeTemplateData = allData.getTestCaseData(menuName='常用通知模板', belongs='updateNoticeTemplate')
    updateNoticeTemplateStatusData = allData.getTestCaseData(menuName='常用通知模板', belongs='updateNoticeTemplateStatus')
    test = Assertions()

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    def teardown_class(self):
        try:
            selectSql = "SELECT id FROM notice_template ORDER BY id DESC LIMIT 0,3"
            self.db.excute(selectSql)
            last3Id = tuple([id[0] for id in self.db.get_all()])
            self.log.info('最新3条模板的id为{}'.format(last3Id))
            print('最新3条模板的id为{}'.format(last3Id))
            deleteSql = "DELETE FROM notice_template WHERE id IN {}".format(last3Id)
            self.db.excute(deleteSql)
        except Exception as e:
            self.log.exception(e)
            raise

    @allure.severity("normal")
    @allure.title("查询通知模板列表")
    @pytest.mark.parametrize("data", noticeTemplatePageDate)
    def test_noticeTemplatePage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    # 新建模板
    @allure.severity("normal")
    @pytest.mark.parametrize("data", addMouldData, ids=addMouldIds)
    def test_addNoticeTemplate(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        sendData['noticeTemplate'] = json.dumps(sendData['noticeTemplate'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查看模板详情")
    @pytest.mark.parametrize("data", selectNoticeTemplateData)
    def test_selectNoticeTemplate(self, data):
        sql = "SELECT id FROM notice_template ORDER BY id DESC LIMIT 0,1"
        self.db.excute(sql)
        try:
            id = self.db.get_one()[0]
        except TypeError:
            raise Exception("获取模板id异常")
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

    @allure.severity("normal")
    @allure.title("修改模板详情")
    @pytest.mark.parametrize("data", updateNoticeTemplateData)
    def test_updateNoticeTemplate(self, data):
        sql = "SELECT * FROM notice_template ORDER BY id DESC LIMIT 0,1"
        self.db.excute(sql)
        try:
            sqldata = self.db.get_one()
            id, templateType, templateName, templateContent = sqldata[0], sqldata[1], sqldata[2], sqldata[3]
        except TypeError:
            raise Exception("获取模板id异常")
        except Exception as e:
            self.log.exception(e)
            raise
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        # 如果全为空，则取sql中最新的，否则直接读参数
        if sendData['noticeTemplate']['id'] == '' and sendData['noticeTemplate']['templateType'] == '' and \
                        sendData['noticeTemplate']['templateName'] == '' and sendData['noticeTemplate'][
            'templateName'] == '':
            sendData['noticeTemplate']['id'] = id
            sendData['noticeTemplate']['templateType'] = templateType
            sendData['noticeTemplate']['templateName'] = templateName + '修改'
            sendData['noticeTemplate']['templateContent'] = templateContent + '修改'
        expected = json.loads(data['expected'])
        sendData['noticeTemplate'] = json.dumps(sendData['noticeTemplate'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("修改模板状态")
    @pytest.mark.parametrize("data", updateNoticeTemplateStatusData)
    def test_updateNoticeTemplateStatus(self, data):
        sql = "SELECT id FROM notice_template ORDER BY id DESC LIMIT 0,1"
        self.db.excute(sql)
        try:
            id = self.db.get_one()[0]
        except TypeError:
            raise Exception("获取模板id异常")
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
