#遍历对象的字符串长度
import json

with open('./fin_finetuning/fine_training.json', 'r') as f:
    data = json.load(f)

for obj in data:

    with open('./fin_finetuning/finetraining_len.json', 'r') as f:
        existing_data=json.load(f)

    json_string = json.dumps(obj, indent=4)
    length_data = {"length": len(json_string)}

    existing_data.append(length_data)

    with open('./fin_finetuning/finetraining_len.json', 'w') as f:
        json.dump(existing_data, f, indent=4)
