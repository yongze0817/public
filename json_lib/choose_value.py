#筛选含有特定键值的对象输出
import json


with open('./fin_finetuning/fin_trainingfile4.0.json', 'r') as f:
    json_data = json.load(f)

    
def filter_json_objects(json_data, key_filter_chars, value_filter_chars):
    filtered_objects = []

    for obj in json_data:
        if target_key in obj:
            value = obj[target_key]
            if isinstance(value, str) and any(char in value for char in value_filter_chars):
                filtered_objects.append(obj)

    return filtered_objects


target_key = "instruction"
value_filter_chars = ["adi","bkng","costco","duol","lulu","marvell","meta","mnst","msft","nvda","qcom"]

filtered_objects = filter_json_objects(json_data, target_key, value_filter_chars)

with open('./fin_finetuning/fin_trainingfile6.0.json', 'w') as f:
    json.dump(filtered_objects, f)
