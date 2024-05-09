#查找符合条件的键值对应的序号
import json

with open('./fin_finetuning/finetraining_len.json', 'r') as f:
    data = json.load(f)

# 要处理的键
key_to_check = "length"
# 要查找的数值下限
lower_limit = 2799

# 存储符合条件的数据对应的键的序号
indices = []

# 遍历列表中的每个字典及其对应的序号
for i, item in enumerate(data):
    # 检查键是否存在并且键的值是否大于指定的数值下限
    if key_to_check in item and item[key_to_check] > lower_limit:
        indices.append(i)

# 输出符合条件的数据对应的键的序号
print("Indices of data with value greater than {} in key '{}':".format(lower_limit, key_to_check))
for idx in indices:
    print(idx)
