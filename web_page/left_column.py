import streamlit as st
import os
import sys
# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上一级目录
parent_dir = os.path.dirname(current_dir)
# 将上一级目录添加到 sys.path 中
sys.path.append(parent_dir)
import copy
import traceback
from Handel_pdf.Pdf_Handler import *
from web_page.Util import *

def left_column_content(session_state):
    st.markdown('<div class="left-header"><h2>项目文件上传及指标提取展示</h2></div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("上传Word文档", type=["pdf"], accept_multiple_files=True)
    st.markdown('<div class="left-header"><h3>指标提取结果</h3></div>', unsafe_allow_html=True)
    left_content_placeholder = st.empty()
    st.session_state['left_content_placeholder'] = left_content_placeholder
    # 处理文件上传逻辑
    if not uploaded_files:
        session_state['current_content'] = None
        session_state['left_doc_uploaded'] = False
        session_state['back_up_content'] = None
        session_state['uploaded_files_dict'] = {}
    if not session_state['current_content'] and uploaded_files:
        try:
            for uploaded_file in uploaded_files:
                if uploaded_file.type == "application/pdf":
                    # 保存上传的文件到本地临时目录
                    file_path = os.path.join("Output/temp_uploaded_pdfs", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    session_state['uploaded_files_dict'][uploaded_file.name] = {}
                    session_state['uploaded_files_dict'][uploaded_file.name]['file_path'] = file_path
                    session_state['uploaded_file_count'] += 1
                    print(f"开始处理第{session_state['uploaded_file_count']}个文件 {uploaded_file.name}！")
                    session_state['Handle_input_file_result'] = Handle_input_file(uploaded_file, session_state['metrics_json_file_path'], session_state['title_json_file_path'], session_state['model'])
                    result_dict = session_state['Handle_input_file_result']
                    print(f"第{session_state['uploaded_file_count']}个文件 {uploaded_file.name} 处理完毕！")
                    session_state['count_title'] = result_dict['title_count_dict']
                    session_state['uploaded_files_dict'][uploaded_file.name]['metrics_inverted_index'] = result_dict['metrics_inverted_index']
                    session_state['uploaded_files_dict'][uploaded_file.name]['metrics_with_class_dict'] = result_dict['metrics_with_class_dict']
                    session_state['left_doc_uploaded'] = True
                    session_state['current_content'] = result_dict['metrics_with_class_dict']
                    # 备份原始文档内容
                    session_state['back_up_content'] = copy.deepcopy(result_dict['metrics_with_class_dict'])
        except Exception as e:
            st.error(str(e))
            error_traceback = traceback.format_exc()
            # 打印错误堆栈信息到终端
            print(error_traceback)

    with st.session_state['left_content_placeholder'].container():
        show_json_content(session_state['current_content'])

    return session_state