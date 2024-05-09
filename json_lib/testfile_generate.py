#生成测试数据集
import json
import os
from utils import handle_pdf

from pydantic import create_model
from pydantic.fields import FieldInfo
import json

FINETUNING_PDF='./fin_finetuning/finetuning_pdf_t/'

# 给定的JSON
with open('./fin_finetuning/fin_trainingtest.json', 'r') as f:
    data_list = json.load(f)


files = os.listdir('./fin_finetuning/finetuning_pdf_t')
for file in files:
    if 'bkng' in file:
        company = file.split('.')[0]
        company_name = company.split('_')[0]

        attr_json_path=f'./fin_finetuning/fine_indicators/{company_name}_is.json' 
        attr_json = open(attr_json_path, 'r').read()
        
        indicators = ', '.join(json.loads(attr_json).keys())
        
        new_obj = { 
            "instruction": f"Extract specified financial data of the latest quarter: {indicators} from the given financial report. Financial statement data in those tables, enclosed in parentheses, such numbers are negative, convert them into negative numbers. Pay attention to whether the report specifies the units of the data provided in the tables, such as thousands, millions, or billions, but at the same time, special attention should also be paid to whether these units have exceptions (i.e., which data are not specified by the unit).", 
            "input": handle_pdf(FINETUNING_PDF + company + '.pdf'),  # 使用原数据中的 "input" 键值
            "output": ""}
        data_list.append(new_obj)

with open('./fin_finetuning/fin_trainingtest.json', 'w') as f:
    json.dump(data_list, f, indent=4)
