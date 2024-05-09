#对列表对象下具体的键值排列组合输出1.0
import json
from itertools import combinations

# 给定的JSON
with open('./fin_finetuning/fin_trainingfile1.0.json', 'r') as f:
    data_list = json.load(f)

# 提取特定键下的数据
json_strings = [obj["output"] for obj in data_list]
values = [json.loads(json_string) for json_string in json_strings]
print(values)


# 找到长度为n/2的所有组合
for d in values:
    key_value_pairs = list(d.items())
    n = len(key_value_pairs)
    required_length = n // 2
    for combination in combinations(key_value_pairs, required_length):  # 每个组合包含两个键值对
        json_str = json.dumps(dict(combination), indent=2)
        new_obj = { 
                   "input": "", 
                   "output": json_str}
        data_list.append(new_obj)

with open('./fin_finetuning/fin_trainingfile1.0.json', 'w') as f:
    json.dump(data_list, f, indent=4)



#对列表对象下具体的键值排列组合输出2.0
import json
from itertools import combinations

# 给定的JSON
with open('./fin_finetuning/fin_trainingfile1.0.json', 'r') as f:
    data_list = json.load(f)

# 提取特定键下的数据
json_strings = [obj["output"] for obj in data_list]
values = [json.loads(json_string) for json_string in json_strings]
print(values)


# 找到长度为n/2的所有组合
for d in values:
    key_value_pairs = list(d.items())
    n = len(key_value_pairs)
    required_length = n // 2
    for combination in combinations(key_value_pairs, required_length):  # 每个组合包含两个键值对
        indicators = ', '.join([pair[0] for pair in combination])
        json_str = json.dumps(dict(combination), indent=2)
        new_obj = { 
                   "instruction": f"Extract specified financial data of the latest quarter: {indicators} from the given financial report.Financial statement data in those tables, enclosed in parentheses, such numbers are negative, convert them into negative numbers.Pay attention to whether the report specifies the units of the data provided in the tables, such as thousands, millions, or billions, but at the same time, special attention should also be paid to whether these units have exceptions (i.e., which data are not specified by the unit).", 
                   "output": json_str}
        data_list.append(new_obj)

with open('./fin_finetuning/fin_trainingfile1.0.json', 'w') as f:
    json.dump(data_list, f, indent=4)



#对列表对象下具体的键值排列组合输出3.0
import json
from itertools import combinations

# 给定的JSON
with open('./fin_finetuning/fin_trainingfile1.0.json', 'r') as f:
    data_list = json.load(f)

new_objects = []

# 找到长度为n/2的所有组合
for obj in data_list:
    d = json.loads(obj["output"])
    key_value_pairs = list(d.items())
    n = len(key_value_pairs)
    required_length = n // 2
    for combination in combinations(key_value_pairs, required_length):  # 每个组合包含两个键值对
        indicators = ', '.join([pair[0] for pair in combination])
        json_str = json.dumps(dict(combination), indent=2)
        new_obj = { 
                   "instruction": f"Extract specified financial data of the latest quarter: {indicators} from the given financial report. Financial statement data in those tables, enclosed in parentheses, such numbers are negative, convert them into negative numbers. Pay attention to whether the report specifies the units of the data provided in the tables, such as thousands, millions, or billions, but at the same time, special attention should also be paid to whether these units have exceptions (i.e., which data are not specified by the unit).", 
                   "input": obj["input"],  # 使用原数据中的 "input" 键值
                   "output": json_str}
        new_objects.append(new_obj)

        
data_list.extend(new_objects)
with open('./fin_finetuning/fin_trainingfile1.0.json', 'w') as f:
    json.dump(data_list, f, indent=4)


#对列表对象下具体的键值排列组合输出4.0
import json
from itertools import combinations

# 给定的JSON
with open('./fin_finetuning/fin_trainingfile.json', 'r') as f:
    data_list = json.load(f)

new_objects = []
threshold = 40

# 找到长度为n/2的所有组合
for obj in data_list:
    count = 0
    d = json.loads(obj["output"])
    key_value_pairs = list(d.items())
    n = len(key_value_pairs)
    required_length = n//2
    for combination in combinations(key_value_pairs, required_length):  # 每个组合包含两个键值对
        if count >= threshold:  # 达到阈值时停止迭代
            break
        indicator = ', '.join([pair[0] for pair in combination])
        json_str = json.dumps(dict(combination), indent=2)
        new_obj = { 
                   "instruction": f"Extract specified financial data of the latest quarter: {indicator} from the given financial report. Financial statement data in those tables, enclosed in parentheses, such numbers are negative, convert them into negative numbers. Pay attention to whether the report specifies the units of the data provided in the tables, such as thousands, millions, or billions, but at the same time, special attention should also be paid to whether these units have exceptions (i.e., which data are not specified by the unit).", 
                   "input": obj["input"],  # 使用原数据中的 "input" 键值
                   "output": json_str}
        new_objects.append(new_obj)
        count += 1


data_list.extend(new_objects)
with open('./fin_finetuning/fin_trainingfile2.0.json', 'w') as f:
    json.dump(data_list, f, indent=4)

#对列表对象下具体的键值排列组合输出5.0
import json
import random
from itertools import combinations

# 给定的JSON
with open('./fin_finetuning/fin_trainingfile1.0.json', 'r') as f:
    data_list = json.load(f)

new_objects = []
threshold = 40

# 找到长度为n/2的所有组合
for obj in data_list:  
    d = json.loads(obj["output"])
    key_value_pairs = list(d.items())
    n = len(key_value_pairs)
    required_length = n // 2

    count = 0
    while count < threshold:
        combination = random.sample(key_value_pairs, required_length) # 每个组合包含两个键值对
        indicator = ', '.join([pair[0] for pair in combination])
        json_str = json.dumps(dict(combination), indent=2)
        new_obj = { 
                   "instruction": f"Extract specified financial data of the latest quarter: {indicator} from the given financial report. Financial statement data in those tables, enclosed in parentheses, such numbers are negative, convert them into negative numbers. Pay attention to whether the report specifies the units of the data provided in the tables, such as thousands, millions, or billions, but at the same time, special attention should also be paid to whether these units have exceptions (i.e., which data are not specified by the unit).", 
                   "input": obj["input"],  # 使用原数据中的 "input" 键值
                   "output": json_str}
        new_objects.append(new_obj)
        count += 1


data_list.extend(new_objects)
with open('./fin_finetuning/fin_trainingfile3.0.json', 'w') as f:
    json.dump(data_list, f, indent=4)
