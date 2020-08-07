#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_roleAuthorityManage.py
@time: 2020/5/8 11:13
@desc:账号管理-角色权限管理
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


@allure.epic('账号管理')
@allure.feature("角色权限管理")
class TestRoleAuthority:
    log = Log().getlog()
    db = DB_config()
    test = Assertions()
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    TreeData = allData.getTestCaseData(menuName='角色权限管理', belongs='adminCompanyAndDeptTree')
    RoleListDate = allData.getTestCaseData(menuName='角色权限管理', belongs='RoleList')
    addRoleData = allData.getTestCaseData(menuName='角色权限管理', belongs='addRole')
    updateData = allData.getTestCaseData(menuName='角色权限管理', belongs='updateRole')
    deleteData = allData.getTestCaseData(menuName='角色权限管理', belongs='deleteRole')
    addDeptData = allData.getTestCaseData(menuName='角色权限管理', belongs='addDept')
    delDeptData = allData.getTestCaseData(menuName='角色权限管理', belongs='delDept')

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @allure.severity("normal")  # blocker，critical，normal，minor，trivial 用例级别
    @allure.title("查看机构部门列表树接口")
    @pytest.mark.parametrize("data", TreeData, indirect=False)  # 参数化时以这种形式
    def test_getTree(self, data):
        """查询组织机构列表树"""
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        expected = json.loads(data['expected'])
        r = self.base.sendRequest(apiUrl, requestsMethod)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("查看机构下角色列表接口")
    @pytest.mark.parametrize("data", RoleListDate, indirect=False)  # 参数化时以这种形式
    def test_getRoleList(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @pytest.fixture(scope='class')
    def getNewRoleId(self, request):
        apiUrl = request.param['ApiUrl']
        requestsMethod = request.param['Method']
        sendData = json.loads(request.param['Data'])
        expected = json.loads(request.param['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        return r.json(), sendData, self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("机构下新建角色接口")
    @pytest.mark.dependency(name='addNewRole')
    @pytest.mark.parametrize("getNewRoleId", addRoleData, indirect=True)  # 参数化时以这种形式
    def test_addNewRole(self, getNewRoleId):
        assert getNewRoleId[2]

    @allure.severity("normal")
    @allure.title("更新角色信息接口")
    @pytest.mark.dependency(depends=['addNewRole'])
    @pytest.mark.parametrize("getNewRoleId", addRoleData, indirect=True)
    @pytest.mark.parametrize("data", updateData, indirect=False)
    def test_updatRole(self, getNewRoleId, data):
        lastSendData = getNewRoleId[1]
        departmentId = lastSendData['departmentId']
        roleName = lastSendData['rolename'] + "修改"
        roleId = getNewRoleId[0]['id']
        apiUrl = data['ApiUrl']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        sendData['departmentId'] = departmentId
        sendData['rolename'] = roleName
        sendData['roleId'] = roleId
        requestsMethod = data['Method']
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("删除角色信息接口")
    @pytest.mark.dependency(depends=['addNewRole'])
    @pytest.mark.parametrize("getNewRoleId", addRoleData, indirect=True)  # 参数化时以这种形式
    @pytest.mark.parametrize("deleteData", deleteData, indirect=False)
    def test_deleteRole(self, getNewRoleId, deleteData):
        apiUrl = deleteData['ApiUrl']
        sendData = json.loads(deleteData['Data'])
        sendData['id'] = getNewRoleId[0]['id']
        requestsMethod = deleteData['Method']
        expected = json.loads(deleteData['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @pytest.fixture(scope='class')
    def getDeptId(self, request):
        apiUrl = request.param['ApiUrl']
        requestsMethod = request.param['Method']
        sendData = json.loads(request.param['Data'])
        sendData['data'] = json.dumps(sendData['data'])
        expected = json.loads(request.param['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        return r.json(), sendData, self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("新建部门接口")
    @pytest.mark.dependency(name='addDept')
    @pytest.mark.parametrize("getDeptId", addDeptData, indirect=True)
    def test_addDept(self, getDeptId):
        assert getDeptId[2]

    @allure.severity("normal")
    @allure.title("删除部门接口")
    @pytest.mark.dependency(depends=['addDept'])
    @pytest.mark.parametrize("getDeptId", addDeptData, indirect=True)
    @pytest.mark.parametrize("data", delDeptData, indirect=False)
    def test_delDept(self, getDeptId, data):
        SenddataToJson = json.loads(getDeptId[1]['data'])
        deptName = SenddataToJson['name']
        parentSeriesId = SenddataToJson['parentSeriesId']
        sql = "SELECT id FROM pms_department WHERE `name`='{}' AND parentSeriesId='{}' ORDER BY id DESC LIMIT 0,1".format(
            deptName, parentSeriesId)
        self.db.excute(sql)
        id = self.db.get_one()[0]
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendData['departmentId'] = int(id)
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
