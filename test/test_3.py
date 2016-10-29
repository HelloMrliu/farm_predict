# coding=utf-8
from __future__ import unicode_literals
import os
import codecs


source_file_path = '../source_data/farming.csv'
predict_file_path = '../source_data/product_market.csv'
result_file_path = '../result_data/result_data.csv'

count = 0
memory_dict = dict()
city_set = set()


def sort_dict(source_dict):
    for key in source_dict:
        source_list = source_dict[key]
        new_list = sorted(source_list, key=lambda tun: tun[1])
        source_dict[key] = new_list


def get_list_by_mid(ele_list):
    price_list = list()
    for ele in ele_list:
        price_list.append(float(ele[0]))
    sorted_price_list = sorted(price_list)
    return sorted_price_list[len(sorted_price_list) / 2]


def get_list_by_new(ele_list, stand_time):
    result_list = list()
    for ele in ele_list:
        if int(ele[1]) <= stand_time:
            continue
        result_list.append(ele)
    return result_list


def get_price_set(price_list):
    price_set = set()
    for val in price_list:
        price_set.add(val[0])
    return price_set

with codecs.open(source_file_path, 'r', 'utf-8') as file:
    for line in file:
        if count == 0:
            count += 1
            continue
        data_list = line.strip('\n').split(',')
        mall_id = data_list[1]
        goods_id = data_list[3]
        average_price = data_list[9]
        price_time = ''.join(((data_list[-1]).split('-')))
        key = mall_id + ',' + goods_id
        try:
            value = (average_price, int(price_time))
        except:
            continue
        if key in memory_dict:
            memory_dict[key].append(value)
        else:
            memory_dict[key] = list()
            memory_dict[key].append(value)
        city_set.add(data_list[0])

print len(memory_dict)
sort_dict(memory_dict)


for key in memory_dict:
    price_list = memory_dict[key]
    new_price_list = get_list_by_new(price_list, 20151200)
    memory_dict[key] = new_price_list

id_set = set()
count = 0
with codecs.open(predict_file_path, 'r', 'utf-8') as file:
    for line in file:
        if count == 0:
            count += 1
            continue
        data_list = line.strip('\n').split(',')
        mall_id = data_list[1]
        goods_id = data_list[3]
        times = data_list[-1]
        key = mall_id + ',' + goods_id
        id_set.add(key)

count = 0
for key in id_set:
    val_list = list()
    for ele in memory_dict[key]:
        val_list.append(float(ele[0]))
    max_num = max(val_list)
    min_num = min(val_list)
    if max_num - min_num > 4:
        print key
        count += 1
print count

'''
for key in memory_dict:
    price_list = memory_dict[key]
    new_price_list = get_list_by_new(price_list, 20151200)
    grow_list = list()
    for index in range(len(new_price_list)):
        if index == len(new_price_list) - 1:
            break
        pre = float(new_price_list[index][0])
        aft = float(new_price_list[index + 1][0])
        if pre <= 0.0:
            continue
        grow_list.append((aft-pre) / pre)
    memory_dict[key] = grow_list


id_set = set()
count = 0
with codecs.open(predict_file_path, 'r', 'utf-8') as file:
    for line in file:
        if count == 0:
            count += 1
            continue
        data_list = line.strip('\n').split(',')
        mall_id = data_list[1]
        goods_id = data_list[3]
        times = data_list[-1]
        key = mall_id + ',' + goods_id
        id_set.add(key)

max_num = 0
min_num = 0

for key in id_set:
    if len(memory_dict[key]) == 0:
        continue
    #print str(max(memory_dict[key])) + ';' + str(min(memory_dict[key]))
    if max(memory_dict[key]) > 0.0:
        max_num += 1
        print "max:", memory_dict[key]
    if min(memory_dict[key]) < 0.0:
        min_num += 1

print max_num
print min_num
'''