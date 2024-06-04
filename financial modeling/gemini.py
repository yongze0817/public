"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import hashlib
import google.generativeai as genai
from utils import handle_pdf, gen_class
import json
import instructor
import re
import os
from pysondb import getDb
import openai

genai.configure(api_key="")

# Set up the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]


class FinancialAssistant:

  def gemini_exract(self, company):

      company_name = company.split('_')[0]
      year_quarter = company.split('_')[1]

      print(company)

      currency_prompt = ''
      if company_name in ['baidu', 'beke', 'jd', 'liauto', 'lkncy', 'ntes', 'rlx']:
          currency_prompt = '4. All the data should be in RMB.'
      elif company_name in ['futu']:
          currency_prompt = '4. All the data should be in HKD.'
      else: currency_prompt = '4. All the data should be in USD.'

      if company_name in ['baidu', 'beke', 'jd', 'liauto', 'lkncy', 'ntes', 'rlx']:
        pn_prompt='1. Financial statement data in those tables, enclosed in parentheses, such numbers are negative, convert them into negative numbers.'
      elif company_name in ['futu']:
        pn_prompt='1. Financial value such as expenses and cost enclosed in parentheses, are definetely negative, convert them into negative numbers.'
      
      model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                  #gemini-1.5-flash-latest
                                  #gemini-1.5-pro-latest
                                  #gemini-1.0-pro
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)


      parts=handle_pdf(f"./fin_finetuning/finetuning_pdf/{company}.pdf")
      #print(parts)

      response_model = instructor.Partial[gen_class(attr_json_path=f'./fin_finetuning/fine_indicators/adi_is.json', class_name="adi")]
      
      attr_json_path=f'./fin_finetuning/fine_indicators/{company_name}_is.json'
      with open(attr_json_path, 'r', encoding='utf-8') as f:
            attr_json = json.load(f)
      
      keys_as_strings = [str(key) for key in attr_json.keys()]
      indicators = ', '.join(keys_as_strings)
      print(indicators)

      response = model.generate_content(
              f'''You are given the {year_quarter} financial report on {company_name} and extract the gaap specified financial indicators for {year_quarter} accurately based on the report. \n
              The designated financial indicators are as follows:\n{indicators} from the given financial report. \n
              When extracting specified data, please pay attention to the following points: \n
              1. Financial value such as expenses and cost enclosed in parentheses, are definetely negative, convert them into negative numbers.'
              2. Pay attention to whether the report specifies the units of the data provided in the tables, such as thousands, millions, or billions, but at the same time, special attention should also be paid to whether these units have exceptions (i.e., which data are not specified by the unit) and Just leave the unit into the figures like adding several zeros in the end. \n
              3. Do not confuse similar indicators. Do not fabricate data. Just show 0 if you could not find it.
              {currency_prompt} including per share data.

              response format be "indicator: value".
              the financial report is as follows:
              {parts}''')

      print(json.dumps({"financial_data": response.text}, indent=4))
      
      self.output2json(response.text) 


  def output2json(self, text):
      with open('./fin_finetuning/gemini_test.json','r') as f:
        data = json.load(f)
      
      if '*' in text:
        pattern = r"\*\*(.+?):\*\* (-0-9.)"
      else:
        pattern = r"(.+?):\s*([-0-9.,]+)"
      #[A-Za-z\s\-.,\'\(-0-9\)]+
      matches = re.findall(pattern, text)
      
      # 将键值对转换为字典
      extracted_data = {key.strip(): value.strip().replace(",", "") for key, value in matches}
      print(extracted_data)

      data.append(extracted_data)

      with open('./fin_finetuning/gemini_test.json','w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    fin = FinancialAssistant()
    #script_dir = os.path.dirname(os.path.abspath(__file__))
    #files = os.path.join(script_dir, 'fin_finetuning/finetuning_pdf')
    files = os.listdir('./fin_finetuning/finetuning_pdf')
    for file in files:
        if 'futu' in file:
            company = file.split('.')[0]
            fin.gemini_exract(company=company)
