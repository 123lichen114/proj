import json
def count_title_occurrences(title_json_file_path):
    """
    读取记录标题倒排索引的 JSON 文件，返回一个字典 {标题：总共出现的次数}
    :param title_json_file_path: 标题倒排索引 JSON 文件路径
    :return: 标题及其总出现次数的字典
    """
    try:
        # 读取 JSON 文件
        with open(title_json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        title_count_dict = {}
        existing_data = json_data["data"]

        # 遍历标题倒排索引数据
        for title, file_count_dict in existing_data.items():
            total_count = sum(file_count_dict.values())
            title_count_dict[title] = total_count

        return title_count_dict

    except FileNotFoundError:
        print(f"未找到文件: {title_json_file_path}")
        return {}