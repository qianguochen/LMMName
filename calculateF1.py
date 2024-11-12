# 测试计算F1
import re


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


gpt_method = 'getWordFatOf'
origin_method = 'getKeyWordSetBatch'

gpt_method_list = split_camel_case(gpt_method)
gpt_method_list = [item.lower() for item in gpt_method_list]
origin_method_list = split_camel_case(origin_method)
origin_method_list = [item.lower() for item in origin_method_list]
sorted_gpt_method_list = sorted(gpt_method_list)
sorted_origin_method_list = sorted(origin_method_list)

print(calcu_precision(sorted_gpt_method_list, sorted_origin_method_list))
print(calcu_recall(sorted_gpt_method_list, sorted_origin_method_list), )
