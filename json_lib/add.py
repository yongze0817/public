#指定键下增加特定内容
import json

# Read JSON file
with open('./fin_finetuning/fine_training.json', 'r') as f:
    data = json.load(f)

for obj in data:
    if 'instruction' in obj and isinstance(obj['instruction'], str):
        # Key exists and its value is a string, concatenate new value with existing value
        existing_value = obj['instruction']
        new_value = "Pay attention to whether the report specifies the units of the data provided in the tables, such as thousands, millions, or billions, but at the same time, special attention should also be paid to whether these units have exceptions (i.e., which data are not specified by the unit)."
        obj['instruction'] = existing_value + new_value
    else:
        # Key doesn't exist or its value is not a string, create a new string with the new value
        obj['instruction'] = "new_value"

# Write the modified data back to the JSON file
with open('./fin_finetuning/fine_training.json', 'w') as f:
    json.dump(data, f, indent=4)  # indent for pretty formatting


#指定键下增加特定内容2.0
import json

# Read JSON file
with open('./fin_finetuning/fin_trainingfile.json', 'r') as f:
    data = json.load(f)

for obj in data:
    d = json.loads(obj["output"])
    indicator=', '.join(d.keys())
    if 'instruction' in obj and isinstance(obj['instruction'], str):
        # Key exists and its value is a string, concatenate new value with existing value
        existing_value = obj['instruction']
        new_value = f"Extract specified financial data of the latest quarter: {indicator} from the given financial report. Financial statement data in those tables, enclosed in parentheses, such numbers are negative, convert them into negative numbers. Pay attention to whether the report specifies the units of the data provided in the tables, such as thousands, millions, or billions, but at the same time, special attention should also be paid to whether these units have exceptions (i.e., which data are not specified by the unit).",   
        if isinstance(new_value, tuple):
            new_value = ', '.join(new_value)
        obj['instruction'] = existing_value + new_value
        print(obj['instruction'])
    else:
        # Key doesn't exist or its value is not a string, create a new string with the new value
        obj['instruction'] = "new_value"

# Write the modified data back to the JSON file
with open('./fin_finetuning/fin_trainingfile1.0.json', 'w') as f:
    json.dump(data, f, indent=4)  # indent for pretty formatting
