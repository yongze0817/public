#1.0
import csv
import json

with open('./fin_finetuning/fin_trainingfile6.0.json', 'r') as f:
    json_data = json.load(f)

def merge_keys_and_write_to_csv(json_list, csv_file_path):
    # 合并前两个键为一个键
    for item in json_list:
        item['input_data'] = f"{item['instruction']}_{item['input']}"
        del item['instruction']
        del item['input']

    # 提取表头（列名）
    header = ['input_data'] + list(json_list[0].keys())[:1]  # 保留除了合并键之外的其余键
    print(header)

    # 将 JSON 列表转换为 CSV 格式
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        
        # 写入表头
        writer.writeheader()
        
        # 逐行写入数据
        for item in json_list:
            writer.writerow({key: item[key] for key in header})


csv_file_path = './fin_finetuning/output.csv'

merge_keys_and_write_to_csv(json_data, csv_file_path)



#2.0
import csv
import json

with open('./fin_finetuning/fin_trainingfile6.0.json', 'r') as f:
    json_data = json.load(f)

def json_list_to_csv(json_list, csv_file_path):
    # 提取表头（列名）
    header = json_list[0].keys()

    # 将 JSON 列表转换为 CSV 格式
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        
        # 写入表头
        writer.writeheader()
        
        # 逐行写入数据
        for item in json_list:
            writer.writerow(item)



csv_file_path = './fin_finetuning/output.csv'

json_list_to_csv(json_data, csv_file_path)
