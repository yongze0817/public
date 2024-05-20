import csv
import random

def extract_random_100_rows_and_merge(input_csv_path, output_csv_path):
    # 读取全部行数据
    all_rows = []
    with open(input_csv_path, 'r', newline='', encoding='latin1') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # 读取表头
        all_rows.append(header)  # 将表头添加到 all_rows 中
        for row in reader:
            all_rows.append(row)  # 将剩余行数据添加到 all_rows 中

    # 随机抽取100条记录
    random_sample = random.sample(all_rows[25:], 25)

    # 合并前25条记录和随机抽取的100条记录
    merged_rows = all_rows[:25] + random_sample

    # 将合并的记录写入输出的 CSV 文件
    with open(output_csv_path, 'w', newline='', encoding='latin1') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(merged_rows)

# 假设 input_csv_path 是你的 CSV 文件路径，output_csv_path 是输出的 CSV 文件路径
input_csv_path = './fin_finetuning/output.csv'
output_csv_path = './fin_finetuning/output1.0.csv'

extract_random_100_rows_and_merge(input_csv_path, output_csv_path)
