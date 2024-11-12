import argparse
import configparser
import json


def load_judge(path):
    had_judge = []
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
        print(len(data))
        for i in data:
            method_info = json.loads(i)
            had_judge.append(method_info)
        f.close()
    return had_judge


def write_judged(line, path):
    line = json.dumps(line)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def judge_method(check_data):
    for i in range(len(check_data)):
        item = check_data[i]
        origin_name = item['origin_name']
        method_body = item['method_body']
        gpt_name = item['gpt_name']
        # judge = item['judge']
        if 'judge' not in item.keys():
            print('gpt_name:' + gpt_name)
            print('origin_name:' + origin_name)
            print(method_body)
            print("===================")
            text = input("输入判断结果(better or worse)：")
            if text == 'better':
                item['judge'] = 'better'
                check_data[i] = item
            elif text == 'worse':
                item['judge'] = 'worse'
                check_data[i] = item
            else:
                print('If the fault is interrupted unexpectedly, run the judgement.sh command to continue the judgment')
                break


def judge_method_content(check_data):
    for i in range(len(check_data)):
        item = check_data[i]
        origin_name = item['signature']['methodName']
        method_body = item['signature']['methodBody']
        gpt_name = item['gpt_name']
        if 'judge' not in item.keys():
            print('gpt_name:' + gpt_name)
            print('origin_name:' + origin_name)
            print(method_body)
            print("===================")
            text = input("输入判断结果(better or worse)：")
            if text == 'better':
                item['judge'] = 'better'
                check_data[i] = item
            elif text == 'worse':
                item['judge'] = 'worse'
                check_data[i] = item
            else:
                print('If the fault is interrupted unexpectedly, run the judgement.sh command to continue the judgment')
                break


def clear_file(path):
    with open(path, 'r+') as f:
        f.truncate(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    config = configparser.ConfigParser()
    config.read('config.ini')
    file = config.get('GPT', 'DATA_SAVE_DIR')
    dir = config.get('GPT', 'PROJECT_DIR')
    parser.add_argument("--contain_content", dest="contain_content", action='store_true')
    args = parser.parse_args()
    contain_content = args.contain_content
    if contain_content:
        data_path = file + 'result_' + dir.strip('/').split('/')[-1] + '_content_tagged.csv'
    else:
        data_path = file + 'result_' + dir.strip('/').split('/')[-1] + '_tagged.csv'
    data = load_judge(data_path)

    if contain_content:
        judge_method_content(data)
    else:
        judge_method(data)
    clear_file(data_path)
    for item in data:
        write_judged(item, data_path)
