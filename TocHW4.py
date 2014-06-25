import json
import urllib.request
import sys
import re

def findTheNameOfRoad(address):
    position = 0
    position_for_road = address.find(match_with_road)
    position_for_avenue = address.find(match_with_avenue)
    position_for_street = address.find(match_with_street)
    if position < position_for_road:
        position = position_for_road
    if position < position_for_avenue:
        position = position_for_avenue
    if position < position_for_street:
        position = position_for_street
    return position

if __name__ == '__main__':
    
    #if(len(sys.argv) < 2):
    #   sys.exit("Error\nusage: python3 <file_name.py> <URL>")
    #else:
    #    url = sys.argv[1]
    #    data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        url = 'http://www.datagarage.io/api/5385b858e7259bb37d926912'
        data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        
        trade_record = dict()
        max_distinct_road = [""]
        number = 0
        max_price = [0]
        min_price = [float('inf')]
        match_with_road = '路'
        match_with_avenue = '大道'
        match_with_street = '街'
        
        for record in data:
            position = findTheNameOfRoad(record['土地區段位置或建物區門牌'])
            if position == 0:
                continue
            name_of_road = record['土地區段位置或建物區門牌'][0:position+1]
            if name_of_road in trade_record:
                if record['交易年月'] in trade_record[name_of_road]:
                    trade_record[name_of_road][record['交易年月']] += 1;
                else:
                    trade_record[name_of_road].update({record['交易年月']:1})
                if record['總價元'] > trade_record[name_of_road]['max_price']:
                    trade_record[name_of_road]['max_price'] = record['總價元']
                if record['總價元'] < trade_record[name_of_road]['min_price']:
                    trade_record[name_of_road]['min_price'] = record['總價元']
            else:
                trade_record[name_of_road] = {record['交易年月']:1, 'max_price':record['總價元'], 'min_price':record['總價元']}

            if len(trade_record[name_of_road]) > number:
                if len(max_distinct_road) > 1:
                    del max_distinct_road[1:]
                    del max_price[1:]
                    del min_price[1:]
                number = len(trade_record[name_of_road])
                max_distinct_road[0] = name_of_road
                max_price[0] = trade_record[name_of_road]['max_price']
                min_price[0] = trade_record[name_of_road]['min_price']
            elif name_of_road in max_distinct_road:
                index = max_distinct_road.index(name_of_road)
                if record['總價元'] > max_price[index]:
                    max_price[index] = record['總價元']
                if record['總價元'] < max_price[index]:
                    max_price[index] = record['總價元']
            elif len(trade_record[name_of_road]) == number:
                max_distinct_road.append(name_of_road)
                max_price.append(trade_record[name_of_road]['max_price'])
                min_price.append(trade_record[name_of_road]['min_price'])
        
        for i in range(0, len(max_distinct_road), 1):
            print(max_distinct_road[i] + ", 最高成交價: " + str(max_price[i]) + ", 最低成交價: " + str(min_price[i]))

