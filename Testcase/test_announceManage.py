#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_announceManage.py
@time: 2020/5/26 10:06
@desc:消息管理-公告管理
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


@allure.epic('消息管理')
@allure.feature("公告管理")
class TestAnnounceManage:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    getTblNoticePageData = allData.getTestCaseData(menuName='公告管理', belongs='getTblNoticePage')
    getTblNoticePageIds = [i['IDS'] for i in getTblNoticePageData]
    tblNoticeSaveData = allData.getTestCaseData(menuName='公告管理', belongs='tblNoticeSave')
    tblNoticeSaveIds = [i['IDS'] for i in tblNoticeSaveData]
    deleteTblNoticeData = allData.getTestCaseData(menuName='公告管理', belongs='deleteTblNotice')
    test = Assertions()

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @allure.severity("normal")
    # @allure.title("查询列表") 用ids参数区分是机构公告还是系统公告
    @pytest.mark.parametrize("data", getTblNoticePageData, ids=getTblNoticePageIds)
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
    # @allure.title("新建机构公告")用ids参数区分是机构公告还是系统公告
    @pytest.mark.dependency(name='noticeSave')
    @pytest.mark.parametrize("data", tblNoticeSaveData, ids=tblNoticeSaveIds)
    def test_tblNoticeSave(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 数据二次处理
        sendData['sendTime'] = nowTime
        sendData['listeners'] = '$' + str(sendData['listeners']) + '$'
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("删除公告")
    @pytest.mark.dependency(depends=['noticeSave'])
    @pytest.mark.parametrize("data", deleteTblNoticeData)
    def test_deleteTblNotice(self, data):
        sql = "SELECT id FROM tbl_notice WHERE noticeTitle = '自动化测试新建机构公告' or noticeTitle = '自动化测试新建系统公告'  ORDER BY id DESC"
        self.db.excute(sql)
        id = self.db.get_all()
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        try:
            if len(id) == 1:
                sendData['id'] = id[0]
                self.log.info('本次使用参数:%s' % sendData)
                r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
                self.log.info('接口返回值:%s' % r.json())
                print('接口返回值:%s' % r.json())
                self.test.assert_text(r.json(), expected)
            elif len(id) > 1:
                for i in id:
                    sendData['id'] = i[0]
                    self.log.info('本次使用参数:%s' % sendData)
                    r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
                    self.log.info('接口返回值:%s' % r.json())
                    print('接口返回值:%s' % r.json())
                    self.test.verifyExpected(r.json(), expected)
            else:
                raise ValueError('获取公告id异常')
        except TypeError:
            raise Exception("获取需要删除的机构公告id异常")
        except Exception as e:
            self.log.exception(e)
            raise
