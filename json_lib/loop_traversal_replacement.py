#循环遍历替换指定键下的内容
import json

with open('./fin_finetuning/fine_training.json', 'r') as f:
    data = json.load(f)

with open('./fin_finetuning/fine_training1.0.json', 'r') as f:
    base_data = json.load(f)

# 定义等差数列的起始索引、步长和数量
start_index_selected = 195
step_selected = 1
num_sequences_selected = 160
selected_indices = [start_index_selected + i * step_selected for i in range(num_sequences_selected)]

# 指定 base_obj 中的等差序列
start_index_base = 15
step_base = 1
num_sequences_base = 20
base_indices = [start_index_base + i * step_base for i in range(num_sequences_base)]

# 根据指定的索引获取对应的元素
selected_obj = [data[i] for i in selected_indices]

# 循环对应 base_obj 中的序列数
base_obj = []
for i in range(len(selected_obj)):
    index = base_indices[i % num_sequences_base]  # 使用取余操作来循环遍历 base_indices
    base_obj.append(base_data[index])

# 将 base_obj 中的 "input" 字段赋值给 selected_obj 中的 "input" 字段
for i in range(len(selected_indices)):
    selected_obj[i]["input"] = base_obj[i]["input"]

with open('./fin_finetuning/fine_training.json', 'w') as f:
    json.dump(data, f, indent=4)
