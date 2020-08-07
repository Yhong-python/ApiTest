#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_noticeDispose.py
@time: 2020/5/27 14:52
@desc:通知管理-通知配置
'''
import warnings

import allure
import pytest
import time
from Common.Assert import Assertions
from Common.DB import DB_config
from Common.Login import loginAdmin
from Common.logger import Log
from Common.operateYamlAndJson import *
from Conf.Config import Config
from Params.param import GetData

warnings.simplefilter("ignore", ResourceWarning)


@allure.epic('通知管理')
@allure.feature("通知配置")
class TestNoticeDispose:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    getNoticeContentTypeDate = allData.getTestCaseData(menuName='通知配置', belongs='getNoticeContentType')
    listPageNoticePlanData = allData.getTestCaseData(menuName='通知配置', belongs='listPageNoticePlan')
    planInfoNoticeTemplatePageData = allData.getTestCaseData(menuName='通知配置', belongs='planInfoNoticeTemplatePage')
    NoticeTemplateIds = [i['IDS'] for i in planInfoNoticeTemplatePageData]
    noticePlanSaveData = allData.getTestCaseData(menuName='通知配置', belongs='noticePlanSave')
    noticePlanSaveIds = [i['IDS'] for i in noticePlanSaveData]
    test = Assertions()

    # 接口返回值sql校验文件路径
    yamlfilepath = os.path.join((os.path.dirname(os.path.dirname(__file__))), 'VerifyJsonAndSql', 'noticeDispose.yaml')

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

        # 删除planType=1的数据
        deleteNoticePlanTemplateType1 = readYaml(self.yamlfilepath)['data']['setupsql']['deleteNoticePlanTemplateType1']
        self.db.excute(deleteNoticePlanTemplateType1)
        deleteNoticePlanType1 = readYaml(self.yamlfilepath)['data']['setupsql']['deleteNoticePlanType1']
        self.db.excute(deleteNoticePlanType1)


    @allure.severity("normal")
    @allure.title("查询配置内容类型")
    @pytest.mark.parametrize("data", getNoticeContentTypeDate)
    def test_getNoticeContentType(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        expected = json.loads(data['expected'])
        r = self.base.sendRequest(apiUrl, requestsMethod)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("进入场景通知的通知列表")
    @pytest.mark.parametrize("data", listPageNoticePlanData)
    def test_listPageNoticePlan(self, data):
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
    # @allure.title("")通知管理-通知配置-进入场景通知-新增方案，选择的三个类型的通知模板
    @pytest.mark.parametrize("data", planInfoNoticeTemplatePageData, ids=NoticeTemplateIds)
    def test_planInfoNoticeTemplatePage(self, data):
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
    # @allure.title("进入场景通知-新建通知方案")
    @pytest.mark.parametrize("data", noticePlanSaveData, ids=noticePlanSaveIds)
    def test_noticePlanSave(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['noticePlanSave']['verifySql']
            self.db.excute(verifySql)
            dbresult = self.db.get_all()
            planTemplates_db = [i[1] for i in dbresult]
            planType_db = dbresult[0][0]
            assert sendData['planType'] == planType_db, "接口传参与数据库实际值不匹配"
            assert list(int(i) for i in sendData['planTemplates'].split(',')) == planTemplates_db, "接口传参与数据库实际值不匹配"
        time.sleep(3)
