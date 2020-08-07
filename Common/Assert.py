#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: Assert.py
@time: 2020/5/11 15:54
@desc:
'''
import json

from Common.logger import Log


class Assertions:
    def __init__(self):
        self.log = Log().getlog()

    def verifyExpected(self, returnJson, expected):
        try:
            if isinstance(expected, dict):
                assert returnJson == expected, "接口返回值与预期返回值不匹配"
                return True
            elif isinstance(expected, (str, int)):
                assert returnJson['code'] == int(expected), "接口返回业务状态码与预期状态码不匹配"
                return True
            else:
                raise ValueError("{}字段值类型错误".format(expected))

        except Exception as e:
            self.log.exception(e)
            raise

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert code == expected_code
            return True
        except:
            self.log.exception("statusCode error, expected_code is %s, statusCode is %s " % (expected_code, code))
            raise

    def assert_body(self, body, body_key, expected_value):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:
        :return:
        """
        try:
            msg = body[body_key]
            assert msg == expected_value
            return True
        except:
            self.log.exception(
                "Response body msg != expected_msg, expected_msg is %s, body_msg is %s" % (expected_value, msg))
            raise

    def assert_in_text(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            # print(text)
            assert expected_msg in text
            return True

        except:
            self.log.exception("Response body Does not contain expected_msg, expected_msg is %s" % expected_msg)
            raise

    def assert_text(self, body, expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body == expected_msg
            return True

        except:
            self.log.exception("Response body != expected_msg, expected_msg is %s, body is %s" % (expected_msg, body))
            raise


if __name__ == "__main__":
    test = Assertions()
    # test.assert_code(200, 200)
    # body = {'name': 1, "pwd": 2}
    # test.assert_body(body, 'name', 1)
    # test.assert_in_text(body, 'name')
    # test.assert_text(body, {'name': 1, "pwd": 2})
    print(test.verifyExpected({"code": 200}, '200'))
