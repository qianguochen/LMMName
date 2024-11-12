# 统计最终结果
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

count_correct = 0
count_total = 0
count_keyword_consistency = 0
count_keyword_consistency_basic = 0
count_keyword_diff = 0
count_keyword_diff_better = 0
count_keyword_diff_worse = 0
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


def task(line, contain_content):
    global count_correct
    global count_total
    global count_keyword_consistency
    global count_keyword_consistency_basic
    global count_keyword_diff
    global count_keyword_diff_better
    global count_keyword_diff_worse
    global precision_total
    global recall_total
    data = json.loads(line)
    gpt_method = data['gpt_name'].replace('`', '').replace('_', '').strip()
    if contain_content:
        origin_method = data['signature']['methodName'].replace('_', '').strip()
    else:
        origin_method = data['origin_name'].replace('_', '').strip()
    judge = data['judge']
    lock.acquire()
    if judge == 'correct':
        count_total += 1
        count_correct += 1
    elif judge == 'consistency':
        count_total += 1
        count_keyword_consistency += 1
    elif judge == 'consistency_basic':
        count_total += 1
        count_keyword_consistency_basic += 1
    elif judge == 'worse':
        count_total += 1
        count_keyword_diff_worse += 1
        count_keyword_diff += 1
    elif judge == 'better':
        count_total += 1
        count_keyword_diff_better += 1
        count_keyword_diff += 1
    origin_name_split = split_camel_case(origin_method)
    gpt_method_split = split_camel_case(gpt_method)
    origin_name_split_tagged = tagger_words(origin_name_split)
    gpt_method_split_tagged = tagger_words(gpt_method_split)
    precision_total += calcu_precision(gpt_method_split_tagged, origin_name_split_tagged)
    recall_total += calcu_recall(gpt_method_split_tagged, origin_name_split_tagged)
    lock.release()


def file_data(path, contain_content):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.readlines()
        for line in text:
            thread_pool.submit(task(line, contain_content))


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
    file_data(data_path, contain_content)
    print('完全正确:{}'.format(count_correct))
    print('关键词一致：{}'.format(count_keyword_consistency))
    print('关键词基本一致:{}'.format(count_keyword_consistency_basic))
    print('差别较大：{}'.format(count_keyword_diff))
    print('合计：{}'.format(count_total))
    precision = round(precision_total / count_total, 4)
    recall = round(recall_total / count_total, 4)
    print('precision:{}:'.format(precision))
    print('recall:{}'.format(recall))
    f1 = round(2 * precision * recall / (precision + recall), 4)
    print('F1:{}'.format(f1))
    print('优于：{}'.format(count_keyword_diff_better))
    print('略于：{}'.format(count_keyword_diff_worse))
    print((count_keyword_diff_worse + count_keyword_diff_better) == count_keyword_diff)
    print((
                      count_keyword_diff + count_correct + count_keyword_consistency + count_keyword_consistency_basic) == count_total)
