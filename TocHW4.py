# TOC HW4
# TocHW4.py
# Created by Wemy Ju on 25/06/2014.

import json
import urllib.request
import sys
import re

def findTheNameOfRoad(address):
    position = []
    token = ['路', '大道', '街']
    for i in range(0, 3, 1):
        position.append(address.find(token[i]))
    if max(position) <= 0:
        position.append(address.find('巷'))
    return max(position)

def saveRecord(month, price, name_of_road):
    global trade_record, record_id
    
    if name_of_road in trade_record:
        if month in trade_record[name_of_road]:
            trade_record[name_of_road][month] += 1;
        else:
            trade_record[name_of_road].update({month:1})

        if price > trade_record[name_of_road]['max_price']:
            trade_record[name_of_road]['max_price'] = price
        elif price < trade_record[name_of_road]['min_price']:
            trade_record[name_of_road]['min_price'] = price
    else:
        trade_record[name_of_road] = {month:1, 'max_price':price, 'min_price':price, 'id':record_id}
        record_id += 1

def extractRecord(price, name_of_road):
    global trade_record, num_of_month, max_distinct_road, max_price, min_price
    
    if len(trade_record[name_of_road]) > num_of_month:
        if len(max_distinct_road) > 1:  # find a road that have max-distinct trade month
            del max_distinct_road[1:]
            del max_price[1:]
            del min_price[1:]
        num_of_month = len(trade_record[name_of_road])
        max_distinct_road[0] = name_of_road
        max_price[0] = trade_record[name_of_road]['max_price']
        min_price[0] = trade_record[name_of_road]['min_price']
    elif name_of_road in max_distinct_road:
        index = max_distinct_road.index(name_of_road)
        if price > max_price[index]:
            max_price[index] = price
        elif price < min_price[index]:
            min_price[index] = price
    elif len(trade_record[name_of_road]) == num_of_month:
        max_distinct_road.append(name_of_road)
        max_price.append(trade_record[name_of_road]['max_price'])
        min_price.append(trade_record[name_of_road]['min_price'])

if __name__ == '__main__':
    
    if(len(sys.argv) < 2):
       sys.exit("Error\nusage: python3 <file_name.py> <URL>")
    else:
        url = sys.argv[1]
        data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        
        trade_record = dict()
        max_distinct_road = [""]
        max_price = [0]
        min_price = [float('inf')]
        num_of_month = 0
        record_id = 0
        
        for record in data:
            position = findTheNameOfRoad(record['土地區段位置或建物區門牌'])
            if position <= 0:
                continue
            name_of_road = record['土地區段位置或建物區門牌'][0:position+1]
            saveRecord(record['交易年月'], record['總價元'], name_of_road)
            extractRecord(record['總價元'], name_of_road)

        extract_data = []
        for i in range(0, len(max_distinct_road), 1):
            extract_data.append((max_distinct_road[i], max_price[i], min_price[i], trade_record[max_distinct_road[i]]['id']))
        sort_extract_data = sorted(extract_data, key = lambda x : x[3])

        for i in range(0, len(max_distinct_road), 1):
            print(sort_extract_data[i][0] + ", 最高成交價: " + str(sort_extract_data[i][1]) + ", 最低成交價: " + str(sort_extract_data[i][2]))
