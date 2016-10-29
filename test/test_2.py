# coding=utf-8
from __future__ import unicode_literals
import os
import codecs


source_file_path = '../source_data/farming.csv'
predict_file_path = '../source_data/product_market.csv'
result_file_path = '../result_data/result_data.csv'

count = 0
memory_dict = dict()
city_dict = dict()


def sort_dict(source_dict):
    for key in source_dict:
        source_list = source_dict[key]
        new_list = sorted(source_list, key=lambda tun: tun[1])
        source_dict[key] = new_list


def get_list_by_new(ele_list, stand_time):
    result_list = list()
    for ele in ele_list:
        if int(ele[1]) <= stand_time:
            continue
        result_list.append(ele)
    return result_list

with codecs.open(source_file_path, 'r', 'utf-8') as file:
    for line in file:
        if count == 0:
            count += 1
            continue
        data_list = line.strip('\n').split(',')
        city_id = data_list[0]
        mall_id = data_list[1]
        goods_type = data_list[2]
        goods_id = data_list[3]
        average_price = data_list[9]
        price_time = ''.join(((data_list[-1]).split('-')))

        key = city_id + ',' + goods_id

        try:
            value = (average_price, int(price_time))
        except:
            continue
        if key in memory_dict:
            memory_dict[key].append(value)
        else:
            memory_dict[key] = list()
            memory_dict[key].append(value)

print len(memory_dict)
sort_dict(memory_dict)

for key in memory_dict:
    new_price_list = get_list_by_new(memory_dict[key], 20151031)
    memory_dict[key] = new_price_list

for key in memory_dict:
    print key
    print memory_dict[key]