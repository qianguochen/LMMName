import concurrent.futures
import json
import os
import re
import requests
import threading
import sys
import configparser
import argparse

sys.setrecursionlimit(2000)
lock = threading.Lock()

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
api_key = ''
api_url = ''
fail_dict = {}
count_token = 0
result_path = ''


def is_only_english(s):
    pattern = re.compile(r'^[a-zA-Z`0-9_]+$')
    return bool(pattern.match(s))


def parse_info(method_info):
    param_types = method_info['paramTypes']
    param_tokens = method_info['paramTokens']
    method_name = method_info['methodName']
    method_body = method_info['methodBody']
    return_type = method_info['return_type']
    parm_list = '('
    if len(param_types) > 0:
        for i in range(len(param_types)):
            parm_list += param_types[i] + ' ' + param_tokens[i] + ';'
        parm_list += ')'

    # 'Suppose I have a Java method whose return value is: and whose argument list is:. The method body is:,. Predict the most appropriate method name that this method might be given'
    # 无返回值 无参数
    if len(param_types) == 0 and return_type == 'void':
        question = 'Suppose I have a Java method whose method body is "' + method_body + '". Predict the most appropriate method name that this method might be given. Please just answer me a method name. The format is methodName'
        return [question, method_name, method_info]
    # 有返回值 无参数
    if len(param_types) == 0 and return_type != 'void':
        question = 'Suppose I have a Java method whose return value is "' + return_type + '" and the method body is "' + method_body + '". Predict the most appropriate method name that this method might be given. Please just answer me a method name. The format is methodName'
        return [question, method_name, method_info]
    # 无返回值 有参数
    if len(param_types) != 0 and return_type == 'void':
        question = 'Suppose I have a Java method whose argument list is "' + parm_list + '" and the method body is "' + method_body + '". Predict the most appropriate method name that this method might be given. Please just answer me a method name. The format is methodName'
        return [question, method_name, method_info]
    # 有返回值 有参数
    if len(param_types) != 0 and return_type != 'void':
        question = 'Suppose I have a Java method whose return value is "' + return_type + '" and whose argument list is "' + parm_list + '". The method body is:' + method_body + '. Predict the most appropriate method name that this method might be given. Please just answer me a method name. The format is methodName'
        return [question, method_name, method_info]


def retry(fail_method_info):
    json_data = json.dumps(fail_method_info)
    if json_data not in fail_dict.keys():
        fail_dict[json_data] = 1
    else:
        value = fail_dict[json_data]
        fail_dict[json_data] = value + 1
    count_fail = fail_dict[json_data]
    if count_fail < 1000:
        values = parse_info(fail_method_info)
        question = values[0]
        thread_pool.submit(task(question, fail_method_info))


def send_chat_request(message, fail_method_info):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "messages": [{"role": "system", "content": message}],
        "max_tokens": 60,
        'model': 'gpt-4o',
        "temperature": 0.2
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response_json = response.json()
        return response_json
    except Exception as e:
        print("try again send")
        print(e)
        retry(fail_method_info)


def task(question, method_info):
    try:
        response = send_chat_request(question, method_info)
        result = response["choices"][0]["message"]["content"]
        print(result)
        global count_token
        count_token += response["usage"]["total_tokens"]
        if is_only_english(result):
            write_data = {
                'gpt_name': result.strip(),
                'origin_name': method_info['methodName'],
                'method_body': method_info['methodBody']
            }
            try:
                lock.acquire()
                with open(result_path, 'a') as file1:
                    line = json.dumps(write_data)
                    file1.write(line + "\n")
                lock.release()
            except FileNotFoundError:
                print("文件未找到")
        else:
            retry(method_info)
    except Exception as e:
        print(e)
        retry(method_info)


had_predict = {}


def load_had_predict(path):
    if not os.path.exists(path):
        with open(path, 'w') as f1:
            pass
    else:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                method_info = json.loads(line)
                origin_name = method_info['origin_name']
                method_body = method_info['method_body']
                key = (origin_name, method_body)
                if key in had_predict.keys():
                    had_predict[key] = had_predict[key] + 1
                else:
                    had_predict[key] = 1


def read_un_predict_file(path, saved_path):
    load_had_predict(saved_path)
    print('加载完毕！！！')
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            data_dict = json.loads(line)
            origin_name = data_dict['methodName']
            method_body = data_dict['methodBody']
            key = (origin_name, method_body)
            if key in had_predict.keys():
                continue
            else:
                data_question = parse_info(data_dict)
                thread_pool.submit(task(data_question[0], data_question[2]))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config.get('GPT', 'key')
    api_url = config.get('GPT', 'url')
    file = config.get('GPT', 'DATA_SAVE_DIR')
    dir = config.get('GPT', 'PROJECT_DIR')
    data_path = file + dir.strip('/').split('/')[-1] + '.csv'
    result_path = file + 'result_' + dir.strip('/').split('/')[-1] + '.csv'
    read_un_predict_file(data_path, result_path)
    print(len(fail_dict))
    print(count_token)
    for item in fail_dict.keys():
        data = json.dumps(item)
        with open(file + 'fail_method.txt', 'a', encoding='utf-8') as f:
            f.write(item + '\n')
