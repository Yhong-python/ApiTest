#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_systermDistribute.py
@time: 2020/5/29 10:28
@desc:系统配置-派发配置
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


@allure.epic('系统配置')
@allure.feature("派发配置")
class TestSystermDistribute:
    log = Log().getlog()
    db = DB_config()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    getAllCountByRoleIdData = allData.getTestCaseData(menuName='派发配置', belongs='getAllCountByRoleId')
    getCountByRoleIdData = allData.getTestCaseData(menuName='派发配置', belongs='getCountByRoleId')
    getCountByRoleIdIds = [i['IDS'] for i in getCountByRoleIdData]
    getDepartmentListByParentIdData = allData.getTestCaseData(menuName='派发配置', belongs='getDepartmentListByParentId')
    getUserCountsByRoleIdData = allData.getTestCaseData(menuName='派发配置', belongs='getUserCountsByRoleId')
    addRoleData = allData.getTestCaseData(menuName='派发配置', belongs='addRole')
    addRoleIds = [i['IDS'] for i in addRoleData]
    overdueTaskTypeData = allData.getTestCaseData(menuName='派发配置', belongs='overdueTaskType')
    selectRolerData = allData.getTestCaseData(menuName='派发配置', belongs='selectRoler')
    getUsersByRoleIdData = allData.getTestCaseData(menuName='派发配置', belongs='getUsersByRoleId')
    savaData = allData.getTestCaseData(menuName='派发配置', belongs='save')
    deleteData = allData.getTestCaseData(menuName='派发配置', belongs='delete')
    test = Assertions()

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @allure.severity("normal")
    @allure.title("查询所有项目已添加角色数量统计")
    @pytest.mark.parametrize("data", getAllCountByRoleIdData)
    def test_getAllCountByRoleId(self, data):
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
    @pytest.mark.parametrize("data", getCountByRoleIdData, ids=getCountByRoleIdIds)
    def test_getCountByRoleId(self, data):
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
    @allure.title("查询机构下所有角色名称")
    @pytest.mark.parametrize("data", getDepartmentListByParentIdData)
    def test_getDepartmentListByParentId(self, data):
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
    @allure.title("查询角色下所有账号数量")
    @pytest.mark.parametrize("data", getUserCountsByRoleIdData)
    def test_getUserCountsByRoleId(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        # self.test.assert_code(r.json()['code'], 200)
        self.test.verifyExpected(r.json(), expected)

    @pytest.fixture(scope='class')
    def cleanData(self):
        yield
        # 删除添加的所有角色,数据重置
        for roleData in self.addRoleData:
            roleDataToJson = json.loads(roleData['Data'])
            for data in roleDataToJson['data']:
                sql = "DELETE FROM qp_itfin2_data_{}.cpt_partner_distributed WHERE partnerId = {} AND roleId = {} ".format(
                    roleDataToJson['basePartnerId'], data['partnerId'], data['roleId'])
                self.db.excute(sql)

    @allure.severity("normal")
    # 添加派发任务角色
    @pytest.mark.parametrize("data", addRoleData, ids=addRoleIds)
    def test_addRole(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['data'] = json.dumps(sendData['data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        # self.test.assert_code(r.json()['code'], 200)
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("获取逾期管理执行任务常量配置")
    @pytest.mark.parametrize("data", overdueTaskTypeData)
    def test_overdueTaskType(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        expected = json.loads(data['expected'])
        r = self.base.sendRequest(apiUrl, requestsMethod)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @pytest.fixture(scope='class')
    def selectRoler(self, request):
        apiUrl = request.param['ApiUrl']
        requestsMethod = request.param['Method']
        sendData = json.loads(request.param['Data'])
        expected = json.loads(request.param['expected'])
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        # return r.json()
        return r.json(), self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("逾期任务新增派发人员时获取角色列表")
    @pytest.mark.parametrize("selectRoler", selectRolerData, indirect=True)
    def test_selectRoler(self, selectRoler):
        assert selectRoler[1]

    @pytest.fixture(scope='class')
    def getUsersByRoleId(self, selectRoler, request):
        apiUrl = request.param['ApiUrl']
        requestsMethod = request.param['Method']
        sendData = json.loads(request.param['Data'])
        expected = json.loads(request.param['expected'])
        # 取最前面的一条角色数据
        for roleData in selectRoler[0]['data']:
            roleId, roleName = roleData['recid'], roleData['rolename']
            sendData['roleId'], sendData['roleName'] = roleId, roleName
            break
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        # return r.json()
        return self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("逾期任务新增派发人员时根据角色获取账号姓名")
    @pytest.mark.parametrize("selectRoler", selectRolerData, indirect=True)
    @pytest.mark.parametrize("getUsersByRoleId", getUsersByRoleIdData, indirect=True)
    def test_getUsersByRoleId(self, selectRoler, getUsersByRoleId):
        assert getUsersByRoleId

    @allure.severity("normal")
    @allure.title("逾期任务新增派发人员保存")
    @pytest.mark.dependency(name='save')
    @pytest.mark.parametrize("data", savaData)
    def test_sava(self, data, cleanData):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        sendData['data'] = json.dumps(sendData['data'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        # self.test.assert_text(r.json(), expected)
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("逾期任务新增派发人员删除")
    @pytest.mark.dependency(depends=['save'])
    @pytest.mark.parametrize("data", deleteData)
    def test_delete(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        sql = "SELECT id FROM qp_itfin2_data_{}.overdue_task_config ORDER BY id DESC LIMIT 0,1".format(
            sendData['basePartnerId'])
        self.db.excute(sql)
        try:
            id = self.db.get_one()[0]
            sendData['id'] = id
        except TypeError:
            raise Exception("获取逾期派发人员id异常")
        except Exception as e:
            self.log.exception(e)
            raise
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        # self.test.assert_text(r.json(), expected)
        self.test.verifyExpected(r.json(), expected)
