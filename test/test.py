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


def get_list_by_ave(ele_list):
    count = 0
    for ele in ele_list:
        count += float(ele[0])
    return count / len(ele_list)


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

time_dict = dict()
id_set = set()
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
        if key in time_dict:
            time_dict[key].add(times)
        else:
            time_dict[key] = set()
            time_dict[key].add(times)

result_dict = dict()
print len(id_set)


count = 0
for key in id_set:
    if key in memory_dict:
        price_list = memory_dict[key]
        price_set = get_price_set(price_list)

        time_set = time_dict[key]
        if len(price_set) <= 1:
            for time_exp in time_set:
                new_key = key + ',' + time_exp
                price = list(price_set)[0]
                result_dict[new_key] = price
            count += 1

        elif len(price_set) <= 10:
            new_price_list = get_list_by_new(price_list, 20151120)
            new_price_set = get_price_set(new_price_list)
            if len(new_price_set) <= 1:
                print '!!!'
                count += 1
                price = list(price_set)[0]
            else:
                price = get_list_by_mid(get_list_by_new(price_list, 20151200))
                '''
                if price > 10.0:
                    price = get_list_by_ave(get_list_by_new(price_list, 20151200))
                '''
            for time_exp in time_set:
                new_key = key + ',' + time_exp
                result_dict[new_key] = price
    else:
        print key


with codecs.open(result_file_path, 'w', 'utf-8') as write_file:
    for key in result_dict:
        write_file.write(key + ',' + str(result_dict[key]) + '\n')
