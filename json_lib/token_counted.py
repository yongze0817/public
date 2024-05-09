#计算tokens
import tiktoken
import json

with open('./fin_finetuning/fin_trainingfile1.0.json', 'r') as f:
    data = json.load(f)

encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-4-32k")


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

for obj in data:
    with open('./fin_finetuning/training_file/finetraining_len.json', 'r') as f:
        existing_data=json.load(f)
    
    json_string = json.dumps(obj, indent=4)
    token=num_tokens_from_string(json_string, "cl100k_base")
    length_data = {
        "token": token,
        "length": len(json_string)}

    existing_data.append(length_data)

    with open('./fin_finetuning/training_file/finetraining_len.json', 'w') as f:
        json.dump(existing_data, f, indent=4)
    
    print(token)
