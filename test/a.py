import random
import time
import requests
import redis
from rest_framework.utils import json
import sys
import numpy as np
from module.Coverage_get_tool import GetCoverage
from module.Combination import Combination
from module.test import fuzz, option_object, object_dic, option_array, array_dic, post, json_txt, fuzz_success

def test(url,p_location,p_name,value_fuzz,p_id,cov_url):
    ini_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
    flag = 0
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = p_id
    '''
    不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
    path和query 用url直接请求
    header和body用request.post(url, headers=headers)或requests.post(url, data)
    '''
    if p_location == 0:
        url = url.replace('{' + p_name + '}', str(value_fuzz))
    elif p_location == 1:
        # url追加?key1=value1&key2=value2到url后,即查询字符串
        if flag == 0:
            flag = 1
            url = url + "?" + str(p_name) + "=" + str(value_fuzz)
        else:
            url = url + "&" + str(p_name) + "=" + str(value_fuzz)
    elif p_location == 2:
        headers[str(p_name)] = str(value_fuzz)
    elif p_location == 3:
        # 参数组成json字符串 ==> data
        data[str(p_name)] = str(value_fuzz)
    '''Redis存储post过的api_id'''
    post.lpush('api_id_p', p_id)
    # '''配置token'''
    # if '?' in url:
    #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
    # else:
    #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
    print('fuzz  ' + str(p_id) + ' post ' + url)
    response = requests.post(url=url, headers=headers, data=data)
    if response != None:
        response_json = response.json()
        json_txt(response_json)
        # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到MySQL数据库中
        time.sleep(2)
        now_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
        '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
        if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
            # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
            fuzz_success_json_data = json.dumps(fuzz_success_data)
            fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
            fuzz_success_data.clear()
    else:
        pass
    print(response.json())


def post_fuzz_test(api_info,cov_url):
    ini_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    parameter = {}
    for field_info in api_info.req_param:
        if field_info.require:
            parameter[field_info.field_name] = field_info.field_type + str(field_info.location)
    length = len(parameter)
    if length == 1:
        flag = 0
        p_name = parameter.keys()
        p_type = parameter[p_name][:-1]
        p_location = parameter[p_name][-1]
        value_fuzz = fuzz(p_type)
        '''
        不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
        path和query 用url直接请求
        header和body用request.post(url, headers=headers)或requests.post(url, data)
        '''
        if p_location == 0:
            url = url.replace('{' + field_info.field_name + '}', str(value_fuzz))
        elif p_location == 1:
            # url追加?key1=value1&key2=value2到url后,即查询字符串
            if flag == 0:
                flag = 1
                url = url + "?" + str(field_info.field_name) + "=" + str(value_fuzz)
            else:
                url = url + "&" + str(field_info.field_name) + "=" + str(value_fuzz)
        elif p_location == 2:
            headers[str(field_info.field_name)] = str(value_fuzz)
        elif p_location == 3:
            # 参数组成json字符串 ==> data
            data[str(field_info.field_name)] = str(value_fuzz)
        '''Redis存储post过的api_id'''
        post.lpush('api_id_p', api_info.api_id)
        # '''配置token'''
        # if '?' in url:
        #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
        # else:
        #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
        print('fuzz  ' + str(api_info.api_id) + ' post ' + url)
        response = requests.post(url=url, headers=headers, data=data)
        if response != None:
            response_json = response.json()
            json_txt(response_json)
            # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到MySQL数据库中
            time.sleep(2)
            now_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
            '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
            if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                fuzz_success_json_data = json.dumps(fuzz_success_data)
                fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                fuzz_success_data.clear()
        else:
            pass
        print(response.json())
    else:
        a = Combination.get_combine(Combination, parameter.keys())
        for b in a:
            c = list(b)   # c是要改变的参数list
            d = set(parameter.keys())
            e = set(c)
            f = d^e
            g = list(f)   # f是不改变的参数list
            for pa in c:
                pa_location = parameter[pa][-1]
                pa_type = parameter[pa][:-1]
                flag = 0
                value_fuzz = fuzz(pa_type)
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if pa_location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(value_fuzz))
                elif pa_location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(value_fuzz)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(value_fuzz)
                elif pa_location == 2:
                    headers[str(field_info.field_name)] = str(value_fuzz)
                elif pa_location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(value_fuzz)
            for pa in g:
                pa_location = parameter[pa][-1]
                pa_type = parameter[pa][:-1]
                flag = 0
                value_fuzz = fuzz(pa_type)
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if pa_location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(value_fuzz))
                elif pa_location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(value_fuzz)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(value_fuzz)
                elif pa_location == 2:
                    headers[str(field_info.field_name)] = str(value_fuzz)
                elif pa_location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(value_fuzz)
            '''Redis存储post过的api_id'''
            post.lpush('api_id_p', api_info.api_id)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
            print('fuzz  ' + str(api_info.api_id) + ' post ' + url)
            response = requests.post(url=url, headers=headers, data=data)
            if response != None:
                response_json = response.json()
                json_txt(response_json)
                # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到MySQL数据库中
                time.sleep(2)
                now_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
                '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
                if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                    # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                    fuzz_success_json_data = json.dumps(fuzz_success_data)
                    fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                    fuzz_success_data.clear()
            else:
                pass
            print(response.json())



