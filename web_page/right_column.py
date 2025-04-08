import streamlit as st
import os
import sys
# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上一级目录
parent_dir = os.path.dirname(current_dir)
# 将上一级目录添加到 sys.path 中
sys.path.append(parent_dir)
from web_page.Util import *

def right_column_content(session_state):
    st.markdown('<div class="right-header"><h2>内容展示区域</h2></div>', unsafe_allow_html=True)
    tab_selection2 = st.selectbox(
        "选择展示内容:",
        ("标题计数", "指标倒排索引", "PDF 预览")
    )

    right_content_placeholder = st.empty()
    if session_state['left_doc_uploaded']:
        if tab_selection2 == "标题计数":
            session_state["right_doc_content"] = session_state['count_title']
        elif tab_selection2 == "指标倒排索引":
            session_state["right_doc_content"] = session_state['Handle_input_file_result']['All_metric_inverted_index']
        elif tab_selection2 == "PDF 预览":
            if session_state['uploaded_files_dict']:
                selected_file = st.selectbox("选择要预览的 PDF 文件", list(session_state['uploaded_files_dict'].keys()))
                file_path = session_state['uploaded_files_dict'][selected_file]['file_path']
                st_display_pdf(file_path)
                session_state['current_content'] = session_state['uploaded_files_dict'][selected_file]['metrics_with_class_dict']
                with st.session_state['left_content_placeholder'].container():
                    show_json_content(session_state['current_content'])
    else:
        session_state['right_doc_content'] = ""
        right_content_placeholder.empty()
    if 'right_selected_doc' not in session_state:
        session_state['right_selected_doc'] = None

    if session_state["right_doc_content"] and tab_selection2 != "PDF 预览":
        with right_content_placeholder.container():
            show_json_content(session_state['right_doc_content'])

    return session_state