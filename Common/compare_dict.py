#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/21 11:12
# @Author  : wenq
# @File    : compare_dict.py

import json
from Common.logger import Log
logger = Log().getlog()

def recursive_json_loads(data):

    try:
        if isinstance(data, list):
            return [recursive_json_loads(i) for i in data]
        elif isinstance(data, tuple):
            return tuple([recursive_json_loads(i) for i in data])
        elif isinstance(data, dict):
            return Storage({recursive_json_loads(k): recursive_json_loads(data[k]) for k in data.keys()})
        else:
            try:
                obj = json.loads(data)
                if obj == data:
                    return data
            except:
                return data
            return recursive_json_loads(obj)
    except Exception as ex:
        logger.error(str(ex))
        return False

class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'

class compareDict:
    '''
    匹配两个dict是否一致，不需要匹配项内容请用***代替，例如timestamp，token等
    '''

    def __init__(self):
        self.res = 0
        #self.cmp_value = cmp_value  #是否只比较key，不比较内容

    def cmp_dict(self,src_data,dst_data):
        """
        :param src_data:
        :param dst_data:
        :return:
        """

        try:
            if type(src_data) == type(dst_data):
                if isinstance(src_data,dict):
                    if src_data.keys() != dst_data.keys():
                        logger.error(u'在src_data不在dst_data中的key = %s'%repr(set(src_data.keys()).difference(set(dst_data.keys()))))
                        logger.error(u'在dst_data不在src_data中的key = %s'%repr(set(dst_data.keys()).difference(set(src_data.keys()))))
                        self.res += 1
                    for key in src_data:
                        if dst_data.has_key(key):
                            #if src_data[key] != '***':
                            #if type(src_data[key]) == str and  src_data[key].find('***') != -1:
                            if str(type(src_data[key])).startswith("<type 'unicode'>") and  src_data[key].find('***') != -1:
                                logger.warn(u'key = %s 不需要比较'%key)
                            else:
                                logger.info(u'比较key = %s : src_value = %s,dst_value = %s'%(key,src_data[key],dst_data[key]))
                                self.cmp_dict(src_data[key],dst_data[key])
                        else:
                            logger.error('dst_data not has_key : %s'%key)
                            self.res += 1
                elif isinstance(src_data,list):
                    if len(src_data) == len(dst_data):
                        for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
                            logger.info(u'比较list : src_value = %s,dst_value = %s'%(src_list,dst_list))
                            self.cmp_dict(src_list, dst_list)
                    else:
                        logger.error("list len: {} != {},{} != {}".format(len(src_data), len(dst_data),src_data,dst_data))
                        self.res += 1
                else:
                    if src_data != dst_data:
                        logger.error("value: {} != {}".format(src_data, dst_data))
                        self.res += 1
            else:
                logger.error("type: {} != {}, value: {} != {}".format(type(src_data), type(dst_data),(src_data), (dst_data)))
                self.res += 1
        except Exception as ex:
            logger.error(str(ex))
            return False

    def cmp_dict_key_and_type(self,src_data,dst_data):
        """
        :param src_data:
        :param dst_data:
        :return:
        """

        logger.info("src_data = %s" % type(src_data))
        logger.info("dst_data = %s" % type(dst_data))
        logger.info("src_data = %s" % src_data)
        logger.info("dst_data = %s" % dst_data)
        try:
            if type(src_data) == type(dst_data):
                if isinstance(src_data,dict):
                    # if src_data.keys() != dst_data.keys():
                    #     logger.error(u'在期望src_data不在实际dst_data中的key = %s' % repr(
                    #         set(src_data.keys()).difference(set(dst_data.keys()))))
                    #     logger.error(u'在实际dst_data不在期望src_data中的key = %s' % repr(
                    #         set(dst_data.keys()).difference(set(src_data.keys()))))
                    #     self.res += 1
                    for key in src_data:
                        if key not in dst_data.keys():
                            logger.error(u'在期望src_data不在实际dst_data中的key = %s' % repr(
                                set(src_data.keys()).difference(set(dst_data.keys()))))
                            self.res += 1
                        if dst_data.has_key(key):
                            if str(type(src_data[key])).startswith("<type 'unicode'>") and  src_data[key].find('***') != -1:
                                logger.warn(u'key = %s 不需要比较'%key)
                            else:
                                logger.info(u'比较key = %s : src_value = %s,dst_value = %s'%(key,src_data[key],dst_data[key]))
                                self.cmp_dict_key_and_type(src_data[key],dst_data[key])
                        else:
                            logger.error('dst_data not has_key : %s'%key)
                            self.res += 1
                elif isinstance(src_data,list):
                    if len(src_data) == len(dst_data):
                        for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
                            logger.info(u'比较list : src_value = %s,dst_value = %s'%(src_list,dst_list))
                            self.cmp_dict_key_and_type(src_list, dst_list)
                    else:
                        #logger.error("list len: {} != {},{} != {}".format(len(src_data), len(dst_data),src_data,dst_data))
                        #self.res += 1
                        logger.warn("list len: {} != {},{} != {}".format(len(src_data), len(dst_data), src_data, dst_data))

                else:
                    logger.info(u"value: {} == {} 不做比较".format(src_data, dst_data))
            else:
                logger.error("type: {} != {}, value: {} != {}".format(type(src_data), type(dst_data),(src_data), (dst_data)))
                self.res += 1
        except Exception as ex:
            logger.error(str(ex))
            return False


if __name__ == '__main__':
    compare=compareDict()
    n={"a":"1","b":"2","c":"3"}
    m={"a":"1","b":"2","c":"3","d":"4"}
    compare.cmp_dict_key_and_type(m,n)
