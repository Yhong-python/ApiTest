#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test.py
@time: 2020/5/19 13:57
@desc:
'''
from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

jsondata = {
    "code": 200,
    "page": 1,
    "test": 2,
    "list": [
        {'user': 1, 'ab': None},
        {'user': 2, 'ac': 444}
    ]
}

my_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "TestInfo",
    "description": "some information about test",
    "type": "object",
    "minProperties": 2,
    "properties": {
        "code": {
            "type": "integer"
        },
        "page": {
            "type": "integer"
        },
        "test": {
            "type": "integer",
            "enum": [1, 2]
        },
        "list": {
            "type": "array",
            "items": {
                "type": "object",
                "minProperties": 1,
                "properties": {
                    "user": {
                        "type": "integer"
                    }
                },
                "patternProperties": {
                    "^a": {
                        "type": ["integer", 'null']
                    }

                }

            }
        }
    }
}

try:
    validate(instance=jsondata, schema=my_schema)
except SchemaError as e:
    print("验证模式schema出错：\n出错位置：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
except ValidationError as e:
    print("json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
else:
    print("验证成功！")
