import argparse
import configparser
import json
import re
from nltk.tag.stanford import StanfordPOSTagger
import concurrent.futures
import threading

# 配置模型路径
model_path = "english-bidirectional-distsim.tagger"
jar_path = "stanford-postagger-4.2.0.jar"
thread_pool = concurrent.futures.ThreadPoolExecutor()
# 创建标注器对象
tagger = StanfordPOSTagger(model_path, jar_path)
lock = threading.Lock()
count_tagged_gpt = 0
count_tagged_origin = 0

count_total = 0
count_keyword_consistency = 0
count_keyword_consistency_basic = 0
count_keyword_diff = 0
count_keyword_diff_better = 0
count_keyword_diff_worse = 0
count_keyword_diff_un_confirm = 0
precision_total = 0
recall_total = 0


def tagger_words(words):
    checked_words = tagger.tag(words)
    filter_words = []
    for item in checked_words:
        if item[1] == 'IN' or item[1] == 'DT':
            print(words)
            print(item[0] + ':' + item[1])
            continue
        else:
            filter_words.append(item[0].lower())
    return filter_words


def split_camel_case(word):
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)', word)
    return words


def calcu_precision(gpt_method_name, origin_method_name):
    gpt_name_set = set(gpt_method_name)
    origin_name_set = set(origin_method_name)
    intersection_list = list(gpt_name_set.intersection(origin_name_set))
    return round(len(intersection_list) / len(gpt_method_name), 4)


def calcu_recall(gpt_method_name, origin_method_name):
    gpt_name_set = set(gpt_method_name)
    origin_name_set = set(origin_method_name)
    intersection_list = list(gpt_name_set.intersection(origin_name_set))
    return round(len(intersection_list) / len(origin_method_name), 4)


def difference_list(origin, gpt):
    return [item for item in gpt if item not in origin]


def write_method_in_hand(line, save_path):
    with open(save_path, 'a', encoding='utf-8') as f:
        f.write(line)


def task(line, save_path, contain_content):
    global count_tagged_gpt
    global count_tagged_origin
    global count_total
    global count_keyword_consistency
    global count_keyword_consistency_basic
    global count_keyword_diff
    global count_keyword_diff_better
    global count_keyword_diff_worse
    global count_keyword_diff_un_confirm
    global precision_total
    global recall_total

    data = json.loads(line)
    gpt_method = data['gpt_name'].replace('`', '').replace('_', '').strip()
    if contain_content:
        origin_method = data['signature']['methodName'].replace('_', '').strip()
    else:
        origin_method = data['origin_name'].replace('_', '').strip()
    if gpt_method == origin_method:
        data['judge'] = 'correct'
        write_method_in_hand(json.dumps(data) + '\n', save_path)
    else:
        origin_name_split = split_camel_case(origin_method)
        gpt_method_split = split_camel_case(gpt_method)
        origin_name_split_tagged = tagger_words(origin_name_split)
        gpt_method_split_tagged = tagger_words(gpt_method_split)
        # gtp 相对于 origin 的差集
        origin_gpt_difference = difference_list(origin_name_split_tagged, gpt_method_split_tagged)

        lock.acquire()
        precision_total += calcu_precision(gpt_method_split_tagged, origin_name_split_tagged)
        recall_total += calcu_recall(gpt_method_split_tagged, origin_name_split_tagged)

        if len(gpt_method_split_tagged) > 1:
            if len(origin_gpt_difference) == 0:
                count_keyword_consistency += 1
                data['judge'] = 'consistency'
                write_method_in_hand(json.dumps(data) + '\n', save_path)
                count_total += 1
            elif len(origin_gpt_difference) == 1:
                count_keyword_consistency_basic += 1
                data['judge'] = 'consistency_basic'
                write_method_in_hand(json.dumps(data) + '\n', save_path)
                count_total += 1
            else:
                if len(gpt_method_split_tagged) > len(origin_name_split_tagged):
                    count_keyword_diff_better += 1
                    data['judge'] = 'better'
                    write_method_in_hand(json.dumps(data) + '\n', save_path)
                    count_keyword_diff += 1
                    count_total += 1
                elif len(gpt_method_split_tagged) < len(origin_name_split_tagged):
                    count_keyword_diff_worse += 1
                    data['judge'] = 'worse'
                    write_method_in_hand(json.dumps(data) + '\n', save_path)
                    count_keyword_diff += 1
                    count_total += 1
                else:
                    count_keyword_diff_un_confirm += 1
                    write_method_in_hand(line, save_path)
                    count_keyword_diff += 1
                    count_total += 1
        # 当gpt返回结果长度为1时
        else:
            if len(origin_gpt_difference) == 1:
                count_keyword_diff += 1
                count_total += 1
                count_keyword_diff_un_confirm += 1
                write_method_in_hand(line, save_path)
            else:
                if len(origin_name_split_tagged) == 1:
                    count_keyword_consistency += 1
                    data['judge'] = 'consistency'
                    write_method_in_hand(json.dumps(data) + '\n', save_path)
                    count_total += 1
                elif len(origin_name_split_tagged) == 2:
                    count_keyword_consistency_basic += 1
                    data['judge'] = 'consistency_basic'
                    write_method_in_hand(json.dumps(data) + '\n', save_path)
                    count_total += 1
                else:
                    count_keyword_diff += 1
                    count_keyword_diff_worse += 1
                    data['judge'] = 'worse'
                    write_method_in_hand(json.dumps(data) + '\n', save_path)
                    count_total += 1

        lock.release()


def tagger_result(path, save_path, contain_content):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.readlines()
        for line in text:
            thread_pool.submit(task(line, save_path, contain_content))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    file = config.get('GPT', 'DATA_SAVE_DIR')
    dir = config.get('GPT', 'PROJECT_DIR')
    parser = argparse.ArgumentParser()
    parser.add_argument("--contain_content", dest="contain_content", action='store_true')
    args = parser.parse_args()
    contain_content = args.contain_content
    if contain_content:
        data_path = file + 'result_' + dir.strip('/').split('/')[-1] + '_content.csv'
        result_path = file + 'result_' + dir.strip('/').split('/')[-1] + '_content_tagged.csv'
    else:
        data_path = file + 'result_' + dir.strip('/').split('/')[-1] + '.csv'
        result_path = file + 'result_' + dir.strip('/').split('/')[-1] + '_tagged.csv'
    tagger_result(data_path, result_path, contain_content)
    print('关键词一致：{}'.format(count_keyword_consistency))
    print('关键词基本一致:{}'.format(count_keyword_consistency_basic))
    print('差别较大：{}'.format(count_keyword_diff))
    print('合计：{}'.format(count_total))
    print('优于：{}'.format(count_keyword_diff_better))
    print('略于：{}'.format(count_keyword_diff_worse))
    print('人工确定：{}'.format(count_keyword_diff_un_confirm))
    print((count_keyword_diff_un_confirm + count_keyword_diff_worse + count_keyword_diff_better) == count_keyword_diff)
