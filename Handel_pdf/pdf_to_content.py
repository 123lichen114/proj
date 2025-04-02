import os
import re
import json
import openai
from read_pdf import *

def ask_LLMmodel(input, prompt ,model_name = 'gpt4o'):
    if model_name == 'gpt4o':
        askGPT(input, prompt)
def askGPT(input, prompt):
    q = str(input)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": q}
    ]

    # 设置 Azure OpenAI 的 API key 和 Endpoint URL
    api_key = 'd2ca2cab8f0f46da891dec75ae8b38ec'  # 替换为你在 Azure 上创建的 API Key
    endpoint = 'https://coe0522.openai.azure.com/'  # 替换为你的 Endpoint URL

    # 配置 OpenAI 客户端
    openai.api_key = api_key
    openai.api_base = endpoint
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"  # 需要使用 GPT-4 的正确版本

    # 调用 GPT-4o 模型
    response = openai.ChatCompletion.create(
        engine="gpt-4o",  # 使用 GPT-4o 模型
        messages=messages,
        temperature=0
    )
    return response['choices'][0]['message']['content']

def clean_gpt_text_to_json(
        str_with_json,
        file_name,
        output_folder_path="Output/cleaned_gpt_ans_json_result"
):
    # 定义正则表达式模式，匹配 JSON 对象
    #pattern = r'\{[^{}]*(\{[^{}]*\}[^{}]*)*\}'
    pattern = r'{.*}'
    match = re.search(pattern, str_with_json, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            # 1. 将提取的 JSON 字符串转成字典
            data_dict = json.loads(json_str)
            # 2. 将字典存到一个 JSON 文件
            output_filename = os.path.splitext(file_name)[0] + '.json'
            output_file_path = os.path.join(output_folder_path, output_filename)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                # 使用 json.dump 将字典写入文件
                json.dump(data_dict, f, ensure_ascii=False, indent=4)
            return data_dict
        except json.JSONDecodeError:
            print(f"提取的内容 {json_str} 不是有效的 JSON 格式。")
    else:
        print("未找到有效的 JSON 数据。")
        return str_with_json

def pdf_to_target_content(input_file):
    pdf_content, file_name = extract_text_from_pdf(input_file)
    if pdf_content:
        output_folder_path="Output/gpt_input"
        output_filename = os.path.splitext(file_name)[0] + '_gpt_input.txt'
        output_file_path = os.path.join(output_folder_path, output_filename)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            print(f"open {output_file_path}")
            f.write(pdf_content)
        with open('Handel_pdf/prompt.txt', 'r') as f:
            prompt = f.read()
            result = askGPT(pdf_content, prompt)
            cleaned_json_result = clean_gpt_text_to_json(result, file_name)
        return cleaned_json_result, file_name