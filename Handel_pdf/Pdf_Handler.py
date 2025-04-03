import os
import json
from sentence_transformers import SentenceTransformer
import sys
# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将当前目录添加到 sys.path 中
sys.path.append(current_dir)
from pdf_to_content import *
from inverted_index import *
from statistic import *

def Handle_input_file(input_file, metrics_json_file_path, title_json_file_path , model):
    print("call Handle_input_file function")
    cleaned_json_result, source_file_name = pdf_to_target_content(input_file)
    titles_list = cleaned_json_result['titles']
    metrics_dict = cleaned_json_result['metrics']
    metrics_with_class_dict = cleaned_json_result['metrics_classes']
    # 生成指标倒排索引字典
    metrics_inverted_index = build_metric_inverted_index(metrics_dict, source_file_name)
    # 更新指标 JSON 文件
    All_metric_inverted_index = update_metric_inverted_index_json(metrics_inverted_index, metrics_json_file_path , model)
    # 生成标题倒排索引字典
    title_inverted_index = build_title_inverted_index(titles_list, source_file_name)
    # 更新标题 JSON 文件
    All_title_inverted_index = update_title_inverted_index_json(title_inverted_index, title_json_file_path , model)
    title_count_dict = count_title_occurrences(title_json_file_path)
    
    html_content = f"<div> \
    {json.dumps(metrics_inverted_index, ensure_ascii=False, indent=4)} \
    </div>"
    
    result_dict = {
        "titles_list" : titles_list,
        "metrics_dict": metrics_dict,
        "metrics_with_class_dict": metrics_with_class_dict,
        "metrics_inverted_index": metrics_inverted_index,
        "title_inverted_index": title_inverted_index,
        "title_count_dict": title_count_dict,
        "html_content": html_content,
        "All_metric_inverted_index": All_metric_inverted_index,
        "All_title_inverted_index": All_title_inverted_index,
        "source_file_name": source_file_name,
    }
    return result_dict

def init_state(OutputFolder = 'Output/'):
    # 定义指标倒排索引 JSON 数据
    metrics_json_data = {
        "description": "Metric Inverted Index",
        "data": {
            # "metric1": {{"file1":"metric1_range1"}},
            # "metric2": {{"file1":"metric2_range1", "file2":"metric2_range2"}}
        }
    }
    metrics_json_file_path = os.path.join(OutputFolder,"Invered_Index","metrics_inverted_Index.json")

    # 将指标倒排索引 JSON 数据写入文件
    with open(metrics_json_file_path, 'w', encoding='utf-8') as f:
        json.dump(metrics_json_data, f, ensure_ascii=False, indent=4)

    # 定义标题倒排索引 JSON 数据
    title_json_data = {
        "description": "Title Inverted Index",
        "data": {
            # "title1": {{"file1": 1}},
            # "title2": {{"file1": 2, "file2": 1}}
        }
    }
    title_json_file_path = os.path.join(OutputFolder,"Invered_Index","title_inverted_index.json")

    # 将标题倒排索引 JSON 数据写入文件
    with open(title_json_file_path, 'w', encoding='utf-8') as f:
        json.dump(title_json_data, f, ensure_ascii=False, indent=4)


    # 初始化 all_metric_inverted_index.json 文件
    all_metric_inverted_index_path = os.path.join(OutputFolder, "all_metric_inverted_index.json")
    all_metric_inverted_index_data = {}
    with open(all_metric_inverted_index_path, 'w', encoding='utf-8') as f:
        json.dump(all_metric_inverted_index_data, f, ensure_ascii=False, indent=4)
    
    
    # 初始化 SentenceTransformer 模型
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    init_info = {
        "metrics_json_file_path": metrics_json_file_path,
        "title_json_file_path": title_json_file_path,
        "model": model,
    }
    return init_info

if __name__ == "__main__":
    DataFolder = 'data'
    input_file = os.path.join(DataFolder, 'AI检查系统招标文件.pdf')
    metrics_json_file_path, title_json_file_path , model = init_state().values()
    result_dict = Handle_input_file(input_file, metrics_json_file_path, title_json_file_path , model)