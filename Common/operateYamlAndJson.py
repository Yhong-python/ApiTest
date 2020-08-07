#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: operateYamlAndJson.py
@time: 2020/5/19 11:19
@desc:
'''
import json
import os

import ruamel
from ruamel import yaml


def readYaml(yamlpath):
    if os.path.exists(yamlpath):
        with open(yamlpath, 'r', encoding='utf-8') as f:
            content = yaml.load(f, Loader=ruamel.yaml.RoundTripLoader)
            f.close()
        return content
    else:
        print('yaml文件路径不存在')
        # return False
        raise FileNotFoundError('yaml文件路径不存在')


def updateYaml(yamlpath, content):
    with open(yamlpath, "w", encoding="utf-8") as f:
        yaml.dump(content, f, Dumper=yaml.RoundTripDumper, allow_unicode=True)
        f.close()


def readjson(jsonpath):
    if os.path.exists(jsonpath):
        with open(jsonpath, 'r', encoding='utf-8') as f:
            content = json.load(f)
            f.close()
        return content
    else:
        # print('json文件路径不存在')
        # return False
        raise FileNotFoundError('json文件路径不存在')


def updatejson(jsonpath, content):
    with open(jsonpath, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False)
        f.close()


def getApiJsonData(jsonFilePath, apiName):
    allData = readjson(jsonFilePath)
    for jsonData in allData['data']:
        if jsonData['apiName'] == apiName:
            return jsonData['returnJsonData']


if __name__ == "__main__":
    # content=readYaml('contractNoManage.yaml')
    # print(content)
    # print(content.get('data').get('contNumRulePage'))
    # newdata={"name":"yh","list1":[{"t1":1,"t2":2}]}
    # content['data']['contNumRulePage']=newdata
    # updateYaml('contractNoManage.yaml',content)
    # print(content['data']['savecontNumRule']['verifySql'].format(134))
    # print(content['data']['savecontNumRule'])
    # for i in content['data'].keys():
    #     print(content['data']['verifySql'])
    # print(content.get('data').get('belongs'))
    # content['menu1']['api2']='22222'
    # updateYaml('returnJson.yaml',content)
    # a={"爱撒娇的":'1','ada':[1,2,3,]}
    # updatejson('contractNoManage.json',a)
    a = readjson('contractNoManage.json')
    print(a)
    # a['data']['ada']={'name':'1','age':2}
    # updatejson('contractNoManage.json',a)
