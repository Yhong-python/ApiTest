#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: param.py
@time: 2020/5/9 16:40
@desc:各模块的数据获取封装
'''
import os

from Params.readexceltools import Excel_read


class GetData:
    def __init__(self, excelFileName, sheetName):
        datapath = os.path.join(os.path.dirname(__file__), 'ExcelFile')
        filepath = os.path.join(datapath, excelFileName)
        if not os.path.exists(filepath):
            raise FileNotFoundError("请检查%s路径下%s文件是否存在" % (datapath, excelFileName))
        excelData = Excel_read(filepath, sheetName)
        self.allData = excelData.get_dict_data()

    def getMenuData(self, menuName):
        data = []
        allMenuName = ['组织机构管理', '角色权限管理', '员工账号管理', '机构面签记录', '服务项管理', '充值管理', '费用管理',
                       '扣款管理', '认证管理', '公告管理', '广告位管理', '优惠券管理', '业务类型管理', '业务类型分配',
                       '常用通知模板', '通知配置', '派发配置', '派发配置', '合同编号管理', '还款方式管理']
        for menuData in self.allData:
            if menuName not in allMenuName:
                raise Exception("请检查菜单：{}  是否在菜单列表中{}".format(menuName, allMenuName))
            if menuName == menuData['Menu']:
                data.append(menuData)
        return data

    def getTestCaseData(self, menuName, belongs):
        menuData = self.getMenuData(menuName)
        if menuData == []:
            raise ValueError("获取菜单:{}  的数据为空,请检查填写的菜单名称或Excel中是否已添加数据".format(menuName))
        else:
            testCaseDataList = []
            for i in menuData:
                if i['belongs'] == belongs:
                    testCaseDataList.append(i)
            if testCaseDataList == []:
                raise ValueError("菜单：{} 中的{}数据为空".format(menuName, belongs))
            else:
                return testCaseDataList

if __name__ == "__main__":
    a = GetData(excelFileName='admin_api.xlsx', sheetName='Sheet1')
    # print(a.GetOrganizeData())
    # b = a.getMenuData("1")
    print(a.getTestCaseData('通知配置', belongs='planInfoNoticeTemplatePage'))
    # for i in a.getTestCaseData('还款方式管理', belongs='enableOrProhibit'):
    #     print(i['expected'])
    #     print(i['expected']=={'code':200})
