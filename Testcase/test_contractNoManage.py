#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_contractNoManage.py
@time: 2020/6/1 11:04
@desc:合同编号管理
'''
import warnings

import allure
import pytest

from Common.Assert import Assertions
from Common.DB import DB_config
from Common.Login import loginAdmin
from Common.logger import Log
from Common.operateYamlAndJson import *
from Conf.Config import Config
from Params.param import GetData

warnings.simplefilter("ignore", ResourceWarning)


@allure.epic('合同编号管理')
class TestContractNoManage:
    log = Log().getlog()
    db = DB_config()
    uploadAndDownloadFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'UploadAndDownloadFile')
    allData = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    contNumRulePageData = allData.getTestCaseData(menuName='合同编号管理', belongs='contNumRulePage')
    saveContNumRuleData = allData.getTestCaseData(menuName='合同编号管理', belongs='saveContNumRule')
    lookImportPageData = allData.getTestCaseData(menuName='合同编号管理', belongs='lookImportPage')
    contNumRuleInfoData = allData.getTestCaseData(menuName='合同编号管理', belongs='contNumRuleInfo')
    insertOrUpdateContNumData = allData.getTestCaseData(menuName='合同编号管理', belongs='insertOrUpdateContNum')
    enableOrProhibitData = allData.getTestCaseData(menuName='合同编号管理', belongs='enableOrProhibit')
    enableOrProhibitDataIds = [i['IDS'] for i in enableOrProhibitData]
    upImportstatusData = allData.getTestCaseData(menuName='合同编号管理', belongs='upImportstatus')
    upImportstatusDataIds = [i['IDS'] for i in upImportstatusData]
    importRuleDateData = allData.getTestCaseData(menuName='合同编号管理', belongs='importRuleDate')
    getCompanyTreeByBasePartnerIdData = allData.getTestCaseData(menuName='合同编号管理',
                                                                belongs='getCompanyTreeByBasePartnerId')
    departmentPageData = allData.getTestCaseData(menuName='合同编号管理', belongs='departmentPage')
    saveDepartmentCodeData = allData.getTestCaseData(menuName='合同编号管理', belongs='saveDepartmentCode')
    getAreaPageData = allData.getTestCaseData(menuName='合同编号管理', belongs='getAreaPage')
    updateCodeData = allData.getTestCaseData(menuName='合同编号管理', belongs='updateCode')
    exportConfigAreaData = allData.getTestCaseData(menuName='合同编号管理', belongs='exportConfigArea')
    importData = allData.getTestCaseData(menuName='合同编号管理', belongs='importData')  # 这两条会重置数值，影响其他的，所以不执行
    recoveryDefaultData = allData.getTestCaseData(menuName='合同编号管理', belongs='recoveryDefault')  # 这两条会重置数值，影响其他的，所以不执行
    getBankData = allData.getTestCaseData(menuName='合同编号管理', belongs='getBank')
    saveBankData = allData.getTestCaseData(menuName='合同编号管理', belongs='saveBank')
    partnerSpPageData = allData.getTestCaseData(menuName='合同编号管理', belongs='partnerSpPage')
    saveSpCodeData = allData.getTestCaseData(menuName='合同编号管理', belongs='saveSpCode')
    getProductTypeData = allData.getTestCaseData(menuName='合同编号管理', belongs='getProductType')
    saveProductTypeData = allData.getTestCaseData(menuName='合同编号管理', belongs='saveProductType')
    getProductFromData = allData.getTestCaseData(menuName='合同编号管理', belongs='getProductFrom')
    saveProductFromData = allData.getTestCaseData(menuName='合同编号管理', belongs='saveProductFrom')
    test = Assertions()
    # 接口返回值sql校验文件路径
    yamlfilepath = os.path.join((os.path.dirname(os.path.dirname(__file__))), 'VerifyJsonAndSql',
                                'contractNoManage.yaml')
    jsonfilepath = os.path.join((os.path.dirname(os.path.dirname(__file__))), 'VerifyJsonAndSql',
                                'contractNoManage.json')

    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

        addDeleteSql = readYaml(self.yamlfilepath)['data']['savecontNumRule']['deleteSql']  # 删除添加的“自动化新增”规则
        self.db.excute(addDeleteSql)
        # 修改接口数据重置到初始状态
        selectSql = readYaml(self.yamlfilepath)['data']['insertOrUpdateContNum']['resetSql']['selectSql']
        insertSql = readYaml(self.yamlfilepath)['data']['insertOrUpdateContNum']['resetSql']['insertSql']
        updateSql1 = readYaml(self.yamlfilepath)['data']['insertOrUpdateContNum']['resetSql']['updateSql1']
        updateSql2 = readYaml(self.yamlfilepath)['data']['insertOrUpdateContNum']['resetSql']['updateSql2']
        deleteSql = readYaml(self.yamlfilepath)['data']['insertOrUpdateContNum']['resetSql']['deleteSql']
        # 插入数据前先查询数据库里是否有该条记录
        self.db.excute(selectSql)
        if self.db.get_one() == None:  # 没有查到记录时，执行插入
            self.db.excute(insertSql)
        self.db.excute(updateSql1)
        self.db.excute(updateSql2)
        self.db.excute(deleteSql)

        # 修改公司及部门中的编码为null
        resetDeptmentSql = readYaml(self.yamlfilepath)['data']['setupsql']['resetDeptmentSql']
        self.db.excute(resetDeptmentSql)

        # 修改合作车商的编码为null
        resetSpSql = readYaml(self.yamlfilepath)['data']['setupsql']['resetSpSql']
        self.db.excute(resetSpSql)

        # 修改业务类型的编码为null
        resrtProductTypeSql = readYaml(self.yamlfilepath)['data']['setupsql']['resrtProductTypeSql']
        self.db.excute(resrtProductTypeSql)

        # 修改业务来源直客的编码为null
        resrtProductFromSql = readYaml(self.yamlfilepath)['data']['setupsql']['resrtProductFromSql']
        self.db.excute(resrtProductFromSql)

    def teardown_class(self):
        # 修改省市中北京的默认值
        updateAreaSql = readYaml(self.yamlfilepath)['data']['setupsql']['resetAreaSql']
        self.db.excute(updateAreaSql)
        # 修改合作银行中杭州万欧的默认值为null
        resetBankSql = readYaml(self.yamlfilepath)['data']['setupsql']['resetBankSql']
        self.db.excute(resetBankSql)

    @allure.severity("normal")
    @allure.title("合同编号规则列表")
    @pytest.mark.parametrize("data", contNumRulePageData)
    def test_contNumRulePage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # assert r.json()['code'] == expected, '接口返回业务状态码不匹配'
        if r.json()['code'] == 200:  # 状态码200时再进行数据校验
            if r.json()['page']['list'] != []:  # list不为空时校验返回值
                verifySql = (readYaml(self.yamlfilepath)['data']['contNumRulePage']['verifySql']).format(
                    sendData['basePartnerId'],
                    sendData['basePartnerId'],
                    sendData['pageSize'])
                self.db.excute(verifySql)
                dbresult = self.db.get_all()
                for i in range(len(dbresult)):
                    assert dbresult[i][0] == r.json()['page']['list'][i]['id']
                    assert dbresult[i][1] == r.json()['page']['list'][i]['ruleName']
                    assert dbresult[i][2] == r.json()['page']['list'][i]['status']
                    assert dbresult[i][3] == r.json()['page']['list'][i]['applyNum']

    # 这里开始完全校验返回值或数据库中的数据
    @allure.severity("normal")
    @allure.title("新建合同编号规则")
    @pytest.mark.parametrize("data", saveContNumRuleData)
    def test_saveContNumRule(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # assert r.json()['code'] == expected, '接口返回业务状态码不匹配'
        if r.json()['code'] == 200:  # 状态码200时再进行数据校验
            verifySql = (readYaml(self.yamlfilepath)['data']['savecontNumRule']['verifySql']).format(
                sendData['basePartnerId'])
            self.db.excute(verifySql)
            dbresult = self.db.get_one()
            id, ruleName, ruleType = dbresult[0], dbresult[1], dbresult[2]
            assert r.json()['id'] == id, '接口返回的新增合同编号id与数据库中的最新id不一致'
            assert sendData['ruleName'] == ruleName, '新增的合同名称与数据库中的最新名称不一致'
            assert sendData['type'] == ruleType, '新增的合同类型与数据库中的最新类型不一致'

    @allure.severity("normal")
    @allure.title("查询导入的合同编号列表")
    @pytest.mark.parametrize("data", lookImportPageData)
    def test_lookImportPage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = int(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # assert r.json()['code'] == expected, '接口返回业务状态码不匹配'
        if r.json()['code'] == 200:  # 状态码200时再进行数据校验
            verifyJson = getApiJsonData(self.jsonfilepath, 'lookImportPage')
            assert r.json() == verifyJson

    @allure.severity("normal")
    @allure.title("查询合同编号详情")
    @pytest.mark.parametrize("data", contNumRuleInfoData)
    def test_contNumRuleInfo(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # assert r.json()['code'] == expected, '接口返回业务状态码不匹配'
        if r.json()['code'] == 200:  # 状态码200时再进行数据校验
            verifyJson = getApiJsonData(self.jsonfilepath, 'contNumRuleInfo')
            assert r.json() == verifyJson, "接口返回值与预期不符合"

    @allure.severity("normal")
    @allure.title("修改合同编号详情")
    @pytest.mark.parametrize("data", insertOrUpdateContNumData)
    def test_insertOrUpdateContNum(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        sendDatapartnerIdList = [i['partnerId'] for i in sendData['data']['contNumRulePartner']]  # 接口传参中勾选的机构id
        # 接口传参中的合同编号名称，描述，自定义规则
        ruleName = sendData['data']['contNumRule']['ruleName']
        description = sendData['data']['contNumRule']['description']
        customRule = sendData['data']['contNumRule']['customRule']
        isInvalidContract = sendData['data']['contNumRule']['isInvalidContract']
        serialTypeLength = sendData['data']['cumRulePlaceholder'][0]['serialTypeLength']
        sendData['data'] = json.dumps(sendData['data'])
        sendData['placeHolderList'] = json.dumps(sendData['placeHolderList'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # assert r.json()['code'] == expected, '接口返回业务状态码不匹配'
        if r.json()['code'] == 200:  # 状态码200时再进行数据校验

            verifySql1 = readYaml(self.yamlfilepath)['data']['insertOrUpdateContNum']['verifySql1']
            self.db.excute(verifySql1)
            dbresult = self.db.get_all()
            partnerIdList = [i[4] for i in dbresult]  # 请求接口后，数据库中实际的机构id
            verifySql2 = readYaml(self.yamlfilepath)['data']['insertOrUpdateContNum']['verifySql2']
            self.db.excute(verifySql2)
            sql_serialTypeLength = self.db.get_one()[0]
            sql_ruleName, sql_description, sql_customRule, sql_isInvalidContract = dbresult[0][0], dbresult[0][1], \
                                                                                   dbresult[0][2], dbresult[0][3]
            assert sendDatapartnerIdList == partnerIdList and sql_ruleName == ruleName and sql_description == description and \
                   sql_customRule == customRule and sql_isInvalidContract == isInvalidContract, sql_serialTypeLength == serialTypeLength
            "接口传参与数据库实际值不匹配"

    @allure.severity("normal")
    # @allure.title("启用/禁用合同编号规则")
    @pytest.mark.parametrize("data", enableOrProhibitData, ids=enableOrProhibitDataIds)
    def test_enableOrProhibit(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库status字段值校验
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['enableOrProhibit']['verifySql']
            self.db.excute(verifySql)
            dbresult = self.db.get_one()[0]
            assert sendData['status'] == dbresult, "接口传参与数据库实际值不匹配"

    @allure.severity("normal")
    # @allure.title("作废/恢复导入的合同编号规则")
    @pytest.mark.parametrize("data", upImportstatusData, ids=upImportstatusDataIds)
    def test_upImportstatus(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库status字段值校验
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['upImportstatus']['verifySql']
            self.db.excute(verifySql)
            dbresult = self.db.get_one()[0]
            assert sendData['status'] == dbresult, "接口传参与数据库实际值不匹配"

    @allure.severity("normal")
    @allure.title("导入合同编号")
    @pytest.mark.parametrize("data", importRuleDateData)
    def test_importRuleDate(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads((data['expected']))
        file = {
            'file': ('合同编号模板.xlsx', open(os.path.join(self.uploadAndDownloadFilePath, '合同编号模板.xlsx'), 'rb'))
        }
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData, files=file)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        assert self.test.verifyExpected(r.json(), expected)
        if r.json()['code'] == 200:
            # 返回json值校验
            verifyJson = getApiJsonData(self.jsonfilepath, 'importRuleDate')
            assert r.json() == verifyJson, "接口返回值与预期不符合"

    @allure.severity("normal")
    @allure.title("设置-公司及部门，查询左侧机构树")
    @pytest.mark.parametrize("data", getCompanyTreeByBasePartnerIdData)
    def test_getCompanyTreeByBasePartnerId(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        assert self.test.verifyExpected(r.json(), expected)
        if r.json()['code'] == 200:
            # 返回json校验
            verifyJson = getApiJsonData(self.jsonfilepath, 'getCompanyTreeByBasePartnerId')
            assert r.json() == verifyJson, "接口返回值与预期不符合"

    @allure.severity("normal")
    @allure.title("设置-公司及部门，获取机构部门详情")
    @pytest.mark.parametrize("data", departmentPageData)
    def test_departmentPage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        assert self.test.verifyExpected(r.json(), expected)
        if r.json()['code'] == 200:
            # 返回json校验
            verifyJson = getApiJsonData(self.jsonfilepath, 'departmentPage')
            assert r.json() == verifyJson, "接口返回值与预期不符合"

    @allure.severity("normal")
    @allure.title("设置-公司及部门，保存机构/部门代号")
    @pytest.mark.parametrize("data", saveDepartmentCodeData)
    def test_saveDepartmentCode(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        sendDataList = [(i['id'], str(i['depCode'])) for i in sendData['deptList']]
        sendData['deptList'] = json.dumps(sendData['deptList'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库status字段值校验
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['saveDepartmentCode']['verifySql'].format(
                tuple([i[0] for i in sendDataList]))
            self.db.excute(verifySql)
            dbresult = self.db.get_all()
            assert tuple(sendDataList) == dbresult, "接口传参与数据库实际值不匹配"

    @allure.severity("normal")
    @allure.title("设置-省市，查询省市代号设置列表")
    @pytest.mark.parametrize("data", getAreaPageData)
    def test_getAreaPage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 返回json校验
        if r.json()['code'] == 200:
            verifyJson = getApiJsonData(self.jsonfilepath, 'getAreaPage')

            assert r.json() == verifyJson, "接口返回值与预期不符合"

    @allure.severity("normal")
    @allure.title("设置-省市，修改省市代号设置")
    @pytest.mark.parametrize("data", updateCodeData)
    def test_updateCode(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库status字段值校验
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['updateCode']['verifySql'].format(sendData['id'],
                                                                                              sendData['code'])
            self.db.excute(verifySql)
            dbresult = self.db.get_one()
            assert sendData['id'] == dbresult[0] and sendData['code'] == dbresult[1], "接口传参与数据库实际值不匹配"

    @allure.severity("normal")
    @allure.title("设置-省市，下载数据")
    @pytest.mark.parametrize("data", exportConfigAreaData)
    def test_exportConfigArea(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData)
        assert r.status_code == 200, '接口请求状态码匹配失败'
        try:
            self.log.info('接口返回值:%s' % r.json())
            print('接口返回值:%s' % r.json())
        except Exception:
            with open(os.path.join(self.uploadAndDownloadFilePath, '省市区下载.xls'), 'wb') as f:
                f.write(r.content)
                print('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, '省市区下载.xls')))
                self.log.info('文件保存路径为{}'.format(os.path.join(self.uploadAndDownloadFilePath, '省市区下载.xls')))
        else:
            assert r.json()['code'] == 200, '下载接口返回值异常'

    # 会影响其他用例
    @allure.severity("normal")
    @allure.title("设置-省市，导入数据")
    @pytest.mark.skip("会重置数据库所有数据导致前面的会有问题，这里不执行了")
    @pytest.mark.parametrize("data", importData)
    def test_importData(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        file = {
            'file': ('省市区上传.xlsx', open(os.path.join(self.uploadAndDownloadFilePath, '省市区上传.xlsx'), 'rb'))
        }
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, param=sendData, files=file)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("设置-省市，恢复默认")
    @pytest.mark.skip("会重置数据库所有数据导致前面的会有问题，这里不执行了")
    @pytest.mark.parametrize("data", recoveryDefaultData)
    def test_recoveryDefault(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, data=sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)

    @allure.severity("normal")
    @allure.title("设置-合作银行，查询合作银行代号设置列表")
    @pytest.mark.parametrize("data", getBankData)
    def test_getBank(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 返回json校验
        if r.json()['code'] == 200:
            verifyJson = getApiJsonData(self.jsonfilepath, 'getBank')
            assert r.json() == verifyJson, "接口返回值与预期不符合"

    @allure.severity("normal")
    @allure.title("设置-合作银行，修改合作银行代号设置")
    @pytest.mark.parametrize("data", saveBankData)
    def test_saveBank(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        bankCode = sendData['data'][0]['code']
        sendData['data'] = json.dumps(sendData['data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库status字段值校验
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['saveBank']['verifySql']
            self.db.excute(verifySql)
            dbresult = self.db.get_one()
            assert bankCode == dbresult[0], "接口传参与数据库实际值不匹配"

    @allure.severity("normal")
    @allure.title("设置-合作车商，查询合作车商代号设置列表")
    @pytest.mark.parametrize("data", partnerSpPageData)
    def test_partnerSpPage(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 返回json校验
        if r.json()['code'] == 200:
            verifyJson = getApiJsonData(self.jsonfilepath, 'partnerSpPage')
            assert r.json() == verifyJson, "接口返回值与预期不符合"

    @allure.severity("normal")
    @allure.title("设置-合作车商，修改合作车商代号设置")
    @pytest.mark.parametrize("data", saveSpCodeData)
    def test_saveSpCode(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        spCode = sendData['spList'][0]['spCode']
        sendData['spList'] = json.dumps(sendData['spList'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库status字段值校验
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['saveSpCode']['verifySql']
            self.db.excute(verifySql)
            dbresult = self.db.get_one()
            assert spCode == dbresult[0], "接口传参与数据库实际值不匹配"

    @allure.severity("normal")
    @allure.title("设置-业务类型，查询业务类型代号设置列表")
    @pytest.mark.parametrize("data", getProductTypeData)
    def test_getProductType(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 返回json校验
        if r.json()['code'] == 200:
            verifyJson = getApiJsonData(self.jsonfilepath, 'getProductType')
            assert r.json() == verifyJson, "接口返回值与预期不符合"

    @allure.severity("normal")
    @allure.title("设置-合作车商，修改合作车商代号设置")
    @pytest.mark.parametrize("data", saveProductTypeData)
    def test_saveProductType(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        productTypeCode = sendData['data'][0]['code']
        sendData['data'] = json.dumps(sendData['data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库status字段值校验
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['saveProductType']['verifySql']
            self.db.excute(verifySql)
            dbresult = self.db.get_one()
            assert productTypeCode == dbresult[0], "接口传参与数据库实际值不匹配"

    @allure.severity("normal")
    @allure.title("设置-业务来源，查询业务来源代号设置列表")
    @pytest.mark.parametrize("data", getProductFromData)
    def test_getProductFrom(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 返回json校验
        if r.json()['code'] == 200:
            verifyJson = getApiJsonData(self.jsonfilepath, 'getProductFrom')
            assert r.json() == verifyJson, "接口返回值与预期不符合"

    @allure.severity("normal")
    @allure.title("设置-业务来源，修改业务来源代号设置")
    @pytest.mark.parametrize("data", saveProductFromData)
    def test_saveProductFrom(self, data):
        apiUrl = data['ApiUrl']
        requestsMethod = data['Method']
        sendData = json.loads(data['Data'])
        productFromCode = sendData['data'][0]['code']
        sendData['data'] = json.dumps(sendData['data'])
        expected = json.loads(data['expected'])
        self.log.info('本次使用参数:%s' % sendData)
        r = self.base.sendRequest(apiUrl, requestsMethod, sendData)
        self.log.info('接口返回值:%s' % r.json())
        print('接口返回值:%s' % r.json())
        self.test.verifyExpected(r.json(), expected)
        # 状态码200时再进行数据库status字段值校验
        if r.json()['code'] == 200:
            verifySql = readYaml(self.yamlfilepath)['data']['saveProductFrom']['verifySql']
            self.db.excute(verifySql)
            dbresult = self.db.get_one()
            assert productFromCode == dbresult[0], "接口传参与数据库实际值不匹配"
