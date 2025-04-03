import os
import re
import json
from read_pdf import *
from My_LLM import *
def empty_nested_dict_values(d):
    """
    递归清空嵌套字典中所有的值为空字符串
    :param d: 输入的嵌套字典
    :return: 清空值后的嵌套字典
    """
    if isinstance(d, dict):
        return {k: empty_nested_dict_values(v) for k, v in d.items()}
    return ""
def prompt_design(history_saved_path , use_history=True):
    if use_history:
        all_inverted_index = None
        with open(history_saved_path, 'r', encoding='utf-8') as f:
            all_inverted_index = json.load(f)
            #将字典的值清空，只留下键
            #empty_nested_dict_values(all_inverted_index) 
        prompt = f"""
        ### Instruction:
        你是一个招标文件解析助手，请输出一个json格式，包含了以下内容:
        任务1.**titles**: 一个列表,用户文本中出现的标题(只要一级标题和二级标题)(注意：不要有“第x章”，“第x部分”这类词) ，格式：[title1,title2 .....] 列表内元素不换行。
        
        任务2.**metrics**: 一个字典，详细记录招标文件中出现的所有关键信息指标：指标取值范围或者描述 , 格式we为 {{metric1:range1,metric2:range2......}} 字典的每一项间不要换行。
        具体做法：
        请先阅读 历史倒排索引信息：{all_inverted_index} 学习模板范式,再结合输入文本，给出输入文本对应的**metrics**

        任务3.**metrics_classes** : 一个嵌套字典，根据语义把任务二得到的metrics中的键值对进行适当聚类，格式
        {{
            class_name1:{{metric1:range1,metric2:range2}}，
            class_name2：{{metric3:range3,metric4:range4}} 。。。。。。
        }} 
        例如 关键时间地点类：{{"投标截止时间"：xx年xx月，"开标时间": xx年xx月，"开标地点"：北京市海淀区}} 你需要充分理解这个例子，并拓展到传入进来的文档内容。
        """
        return prompt
    else:
        prompt = ""
        with open('Handel_pdf/prompt.txt' , 'r') as f:
            prompt = f.read()
        return prompt

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
        
        history_saved_path = "Output/all_metric_inverted_index.json"
        prompt = prompt_design(history_saved_path , use_history=True)
        result = ask_LLMmodel(pdf_content , prompt , model_name = 'gpt4o')
        cleaned_json_result = clean_gpt_text_to_json(result, file_name)
        return cleaned_json_result, file_name