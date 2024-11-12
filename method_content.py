import json
import re
from nltk.tag.stanford import StanfordPOSTagger
import concurrent.futures

# 配置模型路径
model_path = "english-bidirectional-distsim.tagger"
jar_path = "stanford-postagger-4.2.0.jar"
thread_pool = concurrent.futures.ThreadPoolExecutor()
# 创建标注器对象
tagger = StanfordPOSTagger(model_path, jar_path)
compete_key = []

precision_total = 0
recall_total = 0
count_total = 0


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


def load_data(path):
    global precision_total
    global recall_total
    global count_total
    data = {}
    with open(path, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            info = json.loads(i)
            count_total += 1
            methodName = info['signature']['methodName']
            methodBody = info['signature']['methodBody']
            gpt_method = info['gptName'].replace('`', '').replace('_', '').strip()
            # origin_method = data['methodName'].replace('_', '').strip()
            origin_method = info['signature']['methodName'].replace('_', '').strip()
            origin_name_split = split_camel_case(origin_method)
            gpt_method_split = split_camel_case(gpt_method)
            origin_name_split_tagged = tagger_words(origin_name_split)
            gpt_method_split_tagged = tagger_words(gpt_method_split)
            precision_total += calcu_precision(gpt_method_split_tagged, origin_name_split_tagged)
            recall_total += calcu_recall(gpt_method_split_tagged, origin_name_split_tagged)
            key = (
                methodName, methodBody, tuple(info['signature']['paramTokens']), tuple(info['signature']['paramTypes']))
            if key in data.keys():
                val = data[key]
                data[key] = val + 1
            else:

                data[key] = 1
    return data


data_list = load_data('tagged_jedit2_content_judge.csv')


# data_list = load_data('jedit2Data/jedit2_origin_content.csv')

def load_data_content(path):
    count_correct = 0
    global count_total
    global precision_total
    global recall_total
    count_keyword_consistency = 0
    count_keyword_consistency_basic = 0
    count_keyword_diff = 0
    count_keyword_diff_better = 0
    count_keyword_diff_worse = 0
    with open(path, 'r', encoding='utf-8') as f:
        data_lines = f.readlines()
        for item in data_lines:
            info = json.loads(item)
            if (info['methodName'], info['methodBody'], tuple(info['paramTokens']),
                tuple(info['paramTypes'])) not in data_list:
                gpt_method = info['gptName'].replace('`', '').replace('_', '').strip()
                # origin_method = info['methodName'].replace('_', '').strip()
                origin_method = info['methodName'].replace('_', '').strip()
                origin_name_split = split_camel_case(origin_method)
                gpt_method_split = split_camel_case(gpt_method)
                origin_name_split_tagged = tagger_words(origin_name_split)
                gpt_method_split_tagged = tagger_words(gpt_method_split)
                precision_total += calcu_precision(gpt_method_split_tagged, origin_name_split_tagged)
                recall_total += calcu_recall(gpt_method_split_tagged, origin_name_split_tagged)
                judge = info['judge']
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

        print(count_total)
        print(count_correct)
        print(count_keyword_consistency)
        print(count_keyword_consistency_basic)
        print(count_keyword_diff_better)
        print(count_keyword_diff_worse)
        print(count_keyword_diff)


# load_data_content('jedit4Data/jedit4_origin_content.csv')
# load_data_content('jedit4Data/jedit4_origin.csv')
# load_data_content('tagged_jedit2_judge.csv')
load_data_content('tagged_jedit2_judge.csv')
print('合计：{}'.format(count_total))
precision = round(precision_total / count_total, 4)
recall = round(recall_total / count_total, 4)
print('precision:{}:'.format(precision))
print('recall:{}'.format(recall))
f1 = round(2 * precision * recall / (precision + recall), 4)
print('F1:{}'.format(f1))