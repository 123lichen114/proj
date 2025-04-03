import base64
import streamlit as st
import json
from sentence_transformers import SentenceTransformer
import os
import shutil

def init_state(OutputFolder = 'Output/'):
    temp_uploaded_pdfs_folder = os.path.join(OutputFolder,'temp_uploaded_pdfs')
    empty_folder(temp_uploaded_pdfs_folder)
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

def dict_to_html(d):
    def process_dict(d, level=0):
        html = ""
        indent = "&nbsp;&nbsp;" * level
        for key, value in d.items():
            if isinstance(value, dict):
                html += f"<p>{indent}{key}:</p>"
                html += process_dict(value, level + 1)
            else:
                html += f"<p>{indent}{key}: {value}</p>"
        return html

    html_content = "<div>"
    html_content += process_dict(d)
    html_content += "</div>"
    return html_content

def st_display_pdf(pdf_file):
    print(f"call st_display_pdf : {pdf_file}")
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

def show_json_content(content):
    try:
        json_content = json.dumps(content, indent=4, ensure_ascii=False)
        st.code(json_content, language="json",line_numbers=True)
    except (TypeError, ValueError):
        # 如果不是 JSON 格式，按普通文本显示
        st.markdown(f"""
        <div style="height: 750px; overflow-y: scroll; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
            {content}
        </div>
        """, unsafe_allow_html=True)

def empty_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')