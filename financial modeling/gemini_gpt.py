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


from langchain_community.document_loaders import UnstructuredURLLoader
import instructor
from openai import AzureOpenAI, OpenAI
from pydantic import BaseModel
from pydantic import Field
from enum import Enum
from pysondb import getDb
from typing import Optional, Union, List
from textwrap import dedent
# from gpt import get_turbo_Azure
import time
import os
import pandas as pd
import json


genai.configure(api_key="AIzaSyAevvXSJeftBpcNFEeMjZ3O6J6FCTG4L_A")

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


      parts=handle_pdf(f"./uploaded_files/{company}.pdf")
      #print(parts)

      indicators_json_path=f'./indicators/brief.json'
      with open(indicators_json_path, 'r', encoding='utf-8') as f:
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
      self.struct_model_data(response.text)


  os.environ["AZURE_OPENAI_ENDPOINT"] = "https://scc-01-eeatus-gpt-group01-model01.openai.azure.com/"
  os.environ["AZURE_OPENAI_API_KEY"] = "a5552ab2d19f422fa2035b0823a6e3c4"

  def _client(self):
        AZURE_OPENAI_API_KEY = 'a5552ab2d19f422fa2035b0823a6e3c4'
        AZURE_OPENAI_ENDPOINT = 'https://scc-01-eeatus-gpt-group01-model01.openai.azure.com/'
        API_VERSION = '2024-03-01-preview'
        AZURE_DEPLOYMENT = 'gpt4-0125-Preview'
        client = instructor.patch(AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY, api_version=API_VERSION, azure_deployment=AZURE_DEPLOYMENT))
        return client
      
  def struct_model_data(self, content):
        
        model_name = 'gpt4-0125-Preview'
        client = self._client()
        
        response_model = instructor.Partial[gen_class(attr_json_path=f'./indicators/brief.json', class_name="brief")]

        response = client.chat.completions.create(
            model=model_name,
            response_model=response_model,
            temperature=0.0,
            messages=[
                {
                    'role': 'system',
                    'content': f'You are an AI assistant capable of accurately extracting specific data from financial reports.',
                },
                {
                    'role': 'user',
                    'content': dedent(f'''
                    Format the given financial information as follows:
                    {content}'''),
                },
            ],
        )
        response = response.model_dump_json(indent=2)

        print(response)

if __name__ == "__main__":
    fin = FinancialAssistant()
    #is_data = fin.get_income_statement()
    #income_statement = fin.data2excel(is_data, 'Income Statement','test2.1', 'C:/Users/yuanma/Desktop/futu_is.xlsx')
    files = os.listdir('./uploaded_files')
    for file in files:
        if 'Q' in file:
            company = file.split('.')[0]
            fin.gemini_exract(company=company)
