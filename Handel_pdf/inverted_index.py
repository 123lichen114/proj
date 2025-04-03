import json
import copy
import numpy as np
import os

def save_template(metrics_dict, file_name ,output_folder = 'Output'):
    # 写入 JSON 文件路径
    output_file_path = os.path.join(output_folder, "all_metric_inverted_index.json")

    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 检查 JSON 文件是否存在
    if os.path.exists(output_file_path):
        # 读取 JSON 文件中的数据
        with open(output_file_path, 'r', encoding='utf-8') as f:
            all_inverted_index = json.load(f)
    else:
        all_inverted_index = {}

    # 将当前处理的文件的 inverted_index 添加到字典中
    all_inverted_index[file_name] = metrics_dict
    # 将更新后的字典写回 JSON 文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(all_inverted_index, f, ensure_ascii=False, indent=4)
    
    
def build_metric_inverted_index(metrics_dict, file_name):
    """
    构建倒排索引
    :param metrics_dict: 指标字典
    :param file_name: 文件名
    :return: 倒排索引字典
    """
    save_template(metrics_dict, file_name)  
    inverted_index = {}  # 使用普通字典
    for metric, range_value in metrics_dict.items():
        if metric not in inverted_index:
            inverted_index[metric] = {}
        inverted_index[metric][file_name] = range_value


    return inverted_index

def update_metric_inverted_index_json(inverted_index, json_file_path , model):
    """
    更新 JSON 文件中的倒排索引数据
    :param inverted_index: 新生成的倒排索引
    :param json_file_path: JSON 文件路径
    """
    try:
        # 读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        back_up_data = copy.deepcopy(json_data["data"])
        existing_data = json_data["data"]

        # 遍历新的倒排索引
        for new_metric, new_files in inverted_index.items():
            found_similar = False
            for existing_metric in back_up_data.keys():
                # 计算语义相似度
                similarity = np.dot(model.encode(new_metric), model.encode(existing_metric))
                if similarity > 0.9:
                    # 合并数据
                    existing_data[existing_metric].update(new_files)
                    found_similar = True
                    break
            if not found_similar:
                # 没有相似的，直接添加
                existing_data[new_metric] = new_files

        # 写回 JSON 文件
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return json_data
    except FileNotFoundError:
        # 如果文件不存在，创建新的 JSON 文件
        json_data = {
            "description": "Metrics Inverted Index",
            "data": inverted_index
        }
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return json_data


def build_title_inverted_index(titles_list, file_name):
    """
    构建标题的倒排索引
    :param titles_list: 标题列表
    :param file_name: 文件名
    :return: 标题倒排索引字典
    """
    title_inverted_index = {}
    for title in titles_list:
        if title not in title_inverted_index:
            title_inverted_index[title] = {}
        if file_name not in title_inverted_index[title]:
            title_inverted_index[title][file_name] = 1
        else:
            title_inverted_index[title][file_name] += 1
    return title_inverted_index

def update_title_inverted_index_json(title_inverted_index, json_file_path , model):
    """
    更新标题倒排索引的 JSON 文件
    :param title_inverted_index: 标题倒排索引
    :param json_file_path: JSON 文件路径
    """
    try:
        # 读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        existing_data = json_data["data"]
        back_up_data = copy.deepcopy(json_data["data"])
        # 遍历新的标题倒排索引
        for new_title, new_files in title_inverted_index.items():
            found_similar = False
            for existing_title in back_up_data.keys():
                # 计算语义相似度
                similarity = np.dot(model.encode(new_title), model.encode(existing_title))
                if similarity > 0.9:
                    # 合并数据
                    for file, count in new_files.items():
                        if file in existing_data[existing_title]:
                            existing_data[existing_title][file] += count
                        else:
                            existing_data[existing_title][file] = count
                    found_similar = True
                    break
            if not found_similar:
                # 没有相似的，直接添加
                existing_data[new_title] = new_files

        # 写回 JSON 文件
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return json_data

    except FileNotFoundError:
        # 如果文件不存在，创建新的 JSON 文件
        json_data = {
            "description": "Title Inverted Index",
            "data": title_inverted_index
        }
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return json_data