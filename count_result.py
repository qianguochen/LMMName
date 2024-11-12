import re
import json

count_total = 0
count_correct = 0
count_keyword_consistency = 0
count_keyword_consistency_basic = 0
count_keyword_diff = 0
count_keyword_diff_better = 0
count_keyword_diff_worse = 0
count_keyword_diff_un_confirm = 0


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


def write_method_in_hand(line):
    with open('filter_correct_jedit2.txt', 'a', encoding='utf-8') as f:
        f.write(line)


with open('F:\\pycharmWorkSpace\\GPTComparisonHeMa\\total_result_jedit2_2_fix.csv', 'r', encoding='utf-8') as f:
    text = f.readlines()
    precision_total = 0
    recall_total = 0
    for line in text:
        data = json.loads(line)
        gpt_method = data['gpt_name'].replace('`', '').strip()
        origin_method = data['methodName'].strip()

        gpt_method_list = split_camel_case(gpt_method)
        gpt_method_list = [item.lower() for item in gpt_method_list]
        origin_method_list = split_camel_case(origin_method)
        origin_method_list = [item.lower() for item in origin_method_list]
        sorted_gpt_method_list = sorted(gpt_method_list)
        sorted_origin_method_list = sorted(origin_method_list)

        precision_total += calcu_precision(sorted_gpt_method_list, sorted_origin_method_list)
        recall_total += calcu_recall(sorted_gpt_method_list, sorted_origin_method_list)

        count_diff = 0
        # 原方法名长度为1
        if len(sorted_origin_method_list) == 1:
            if len(sorted_gpt_method_list) == 1:
                if gpt_method == origin_method:
                    count_correct += 1
                    count_total += 1
                else:
                    count_keyword_diff += 1
                    count_total += 1
                    write_method_in_hand(line)
                    count_keyword_diff_un_confirm += 1

            # 原方法名长度为1 预测方法名长度大于1
            else:
                if sorted_origin_method_list[0] in sorted_gpt_method_list and len(sorted_gpt_method_list) == 2:
                    count_keyword_consistency_basic += 1
                    count_total += 1
                    write_method_in_hand(line)
                else:
                    count_keyword_diff += 1
                    count_keyword_diff_better += 1
                    count_total += 1
                    write_method_in_hand(line)

        else:
            if gpt_method == origin_method:
                count_correct += 1
                count_total += 1
            else:
                # 预测方法名长度与原方法名长度一致
                if len(sorted_origin_method_list) == len(sorted_gpt_method_list):
                    gpt_method_list_str = ''.join(sorted_gpt_method_list)
                    origin_method_list_str = ''.join(sorted_origin_method_list)
                    if gpt_method_list_str == origin_method_list_str:
                        count_keyword_consistency += 1
                        count_total += 1
                        write_method_in_hand(line)
                    else:
                        for item in sorted_origin_method_list:
                            if item not in sorted_gpt_method_list:
                                count_diff += 1
                        if count_diff == 1:
                            count_keyword_consistency_basic += 1
                            count_total += 1
                            write_method_in_hand(line)
                        else:
                            count_keyword_diff += 1
                            # write_method_in_hand(line)
                            count_keyword_diff_un_confirm += 1
                            count_total += 1
                            write_method_in_hand(line)
                # 预测名和原方法名长度不一致
                else:
                    if len(sorted_gpt_method_list) > len(sorted_origin_method_list):
                        for item in sorted_gpt_method_list:
                            if item not in sorted_origin_method_list:
                                count_diff += 1
                        if count_diff == 1:
                            count_keyword_consistency_basic += 1
                            count_total += 1
                            write_method_in_hand(line)
                        else:
                            count_keyword_diff += 1
                            count_keyword_diff_better += 1
                            count_total += 1
                            write_method_in_hand(line)
                    else:
                        for item in sorted_origin_method_list:
                            if item not in sorted_gpt_method_list:
                                count_diff += 1
                        if count_diff == 1:
                            count_keyword_consistency_basic += 1
                            count_total += 1
                            write_method_in_hand(line)
                        else:
                            count_keyword_diff += 1
                            count_keyword_diff_worse += 1
                            count_total += 1
                            write_method_in_hand(line)

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
    print('人工确定：{}'.format(count_keyword_diff_un_confirm))
    print((count_keyword_diff_un_confirm + count_keyword_diff_worse + count_keyword_diff_better) == count_keyword_diff)
