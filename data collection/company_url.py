import requests
from bs4 import BeautifulSoup
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests.exceptions import RequestException
from google.cloud import storage
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

from pathlib import Path
import hashlib
import google.generativeai as genai

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

api_key = 'AIzaSyAXIKhd5YJq6r3gISw-3vQf3-6uxZ-ZjYM'
cse_id = 'e32c3228e733547dc'


products = [
    "ACE Studio", "AI SPEECH", "AIXcoder", "AI Design", "AI PPT .cn", "AI帮个忙", "AI改图", "AI乌托邦", "BimoAI", 
    "CODEFUSE", "Chatmind", "CodeGeeX", "Copilot", "Cubox", "D.DESIGN", "DECA", "Dreamina", "Effidit", "FRIDAY", 
    "Fittern", "FlowUs", "GitHub Copilot", "GitMind", "MasterGo", "My AI", "PIC Copilot", "PixWeaver", "Pixso", 
    "ProcessOn", "SKY", "TME Studio", "VERSE", "WriteWise", "alibaba WOOD", "chatppt", "iSlide"
]
def google_search(query, api_key, cse_id, num=1):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}&num={num}"
        response = requests.get(url)
        response.raise_for_status()  # 如果响应有错误会抛出HTTPError
        results = response.json()
        return results.get('items', [])
    except HttpError as http_err:
        print(f'HTTP error occurred: {http_err}')  # HTTP错误（如401，403等）
    except RequestException as req_err:
        print(f'Request error occurred: {req_err}')  # 其他请求错误（如连接错误等）
    except Exception as err:
        print(f'Other error occurred: {err}')  # 其他错误
    return []

def gemini_exract(product,title):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                  #gemini-1.5-flash-latest
                                  #gemini-1.5-pro-latest
                                  #gemini-1.0-pro
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    
    response = model.generate_content(
        f'''according to {title}, extract the company which release the {product}
        if could not find the data, please return ' '
        response format be '{product}: company_name
        ''')
    print(response.text)
    output2csv(response.text)


def output2csv(text):
    excel_file_path = 'C:/Users/yuanma/Desktop/company_name.xlsx'      
    pattern = r"(.+?):\s*([\s\S]+)"
    matches = re.findall(pattern, text)
    company_data = {key.strip(): value.strip().replace(",", "") for key, value in matches}
    df = pd.DataFrame(list(company_data.items()), columns=["产品名", "公司名"])
    try:
        existing_data = pd.read_excel(excel_file_path)
        combined_df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        combined_df = df
    with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='w') as writer:
        combined_df.to_excel(writer, sheet_name='Sheet1', index=False)
    print("Data successfully appended to the Excel file.")


# 初始化字典以存储产品和第一个链接
product_to_links = {}
# 执行搜索并获取前五个链接
for product in products:
    query = f"{product}"
    try:
        results = google_search(f"{product}", api_key, cse_id, num=10)
        results += google_search(f"AI工具集{product}", api_key, cse_id, num=10)
        if results:
            links = [result['link'] for result in results[:20]]
            product_to_links[product] = links
        else:
            product_to_links[product] = ["未找到"]
        print(f"产品：{product}, 前五个链接：{product_to_links[product]}")
    except Exception as e:
        print(f"产品：{product}, 获取链接失败：{e}")
        product_to_links[product] = ["获取链接失败"]

# 将字典转换为DataFrame
product_to_links_df = pd.DataFrame([(product, *links) for product, links in product_to_links.items()], 
                                   columns=["产品名","链接1", "链接2", "链接3", "链接4", "链接5"])

# 使用melt函数将链接列重塑为行
product_to_links_df = product_to_links_df.melt(id_vars=['产品名'], value_vars=["链接1", "链接2", "链接3", "链接4", "链接5"], 
                                               var_name="链接序号", value_name="链接")

# 将产品名列设置为索引项
product_to_links_df = product_to_links_df.set_index('产品名')
with pd.ExcelWriter('product_to_links.xlsx', engine='openpyxl', mode='w') as writer:
    product_to_links_df.to_excel(writer, index=False)
# 打印DataFrame
print(product_to_links_df)


# 初始化字典以存储产品和网页内容
product_to_content = {}


# 设置Selenium WebDriver
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 读取每个链接的网页内容
for product, links in product_to_links.items():
    for link in links:
        if link not in ["未找到", "获取链接失败"]:
            try:
                response = requests.get(link)
                response.raise_for_status()
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                # 尝试从常见标签中提取内容
                content = soup.find('article')
                if not content:
                    content = soup.find('div', {'class': 'main-content'})
                if not content:
                    content = soup.find('div')
                if content:
                    paragraphs = [p.get_text() for p in content.find_all('p')]
                    if not paragraphs:
                        raise ValueError("内容为空")
                    product_to_content[product] += "\n".join(paragraphs)
                else:
                    raise ValueError("未找到主要内容")
            except Exception as e:
                print(f"产品：{product},{link} 静态获取内容失败：{e}，尝试动态获取")
                # 动态获取内容
                try:
                    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
                        driver.get(link)
                        time.sleep(5)  # 等待页面加载

                        # 滚动到页面底部以触发所有内容加载
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)

                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        content = soup.find('article')
                        if not content:
                            content = soup.find('div', {'class': 'main-content'})
                        if not content:
                            content = soup.find('div')
                        if content:
                            paragraphs = [p.get_text() for p in content.find_all('p')]
                            if paragraphs:
                                product_to_content[product] += "\n".join(paragraphs)
                            else:
                                product_to_content[product] = "未找到主要内容"
                        else:
                            product_to_content[product] = "未找到主要内容"
                except Exception as e:
                    print(f"产品：{product},{link} 动态获取内容失败：{e}")
                    product_to_content[product] = "获取内容失败"
        else:
            product_to_content[product] += link

    print(f"产品：{product}, 网页内容：{product_to_content[product]}")    
    gemini_exract(product,product_to_content[product])


product_to_content_df = pd.DataFrame(list(product_to_content.items()), columns=["产品名", "网页内容"])
product_to_content_df.to_csv('product_to_content.csv', index=False)

# 打印DataFrame
print(product_to_content_df)
