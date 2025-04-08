import streamlit as st
import os
import sys
# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上一级目录
parent_dir = os.path.dirname(current_dir)
# 将上一级目录添加到 sys.path 中
sys.path.append(parent_dir)
from web_page.Util import init_state

def init_web(session_state):
    # 设置页面为宽布局
    st.set_page_config(page_title="标书梳理", layout="wide")
    # 注入自定义 CSS 控制代码块换行
    st.markdown("""
    <style>
    /* 针对所有 st.code 块生效 */
    .stCode pre {
        white-space: pre-wrap !important;  /* 保留空格和换行，允许单词内换行 */
        /* 或使用 pre-line：合并多余空格，允许单词内换行 */
        /* white-space: pre-line !important; */
        overflow-x: visible !important;   /* 隐藏横向滚动条 */
        max-width: 100%;                  /* 宽度占满容器 */
        word-wrap: break-word !important; /* 兼容旧浏览器 */
    }
    </style>
    """, unsafe_allow_html=True)

    logo_path = './web_resource/logo.jpg'
    st.image(logo_path, width=200)
    st.markdown("<h1 style='text-align: center;'>标书梳理</h1>", unsafe_allow_html=True)
    # 使用自定义 CSS 来居中标题
    st.markdown("""
        <style>
            .left-header {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
                text-align: center;
            }
            .right-header {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)
    # 初始化状态
    if 'first_doc_uploaded' not in st.session_state:
        st.session_state['first_doc_uploaded'] = True
    if 'left_doc_uploaded' not in st.session_state:
        st.session_state['left_doc_uploaded'] = False
    if 'right_doc_content' not in st.session_state:
        st.session_state['right_doc_content'] = ""
    if 'right_doc_error' not in st.session_state:
        st.session_state['right_doc_error'] = ""
    if 'matches' not in st.session_state:
        st.session_state['matches'] = []
    if 'current_index' not in st.session_state:
        st.session_state['current_index'] = -1
    if 'first_render' not in st.session_state:
        st.session_state['first_render'] = True
    if 'uploaded_file_count' not in st.session_state:
        st.session_state['uploaded_file_count'] = 0
    if 'init_info' not in st.session_state:
        st.session_state['init_info'] = init_state()
        st.session_state['metrics_json_file_path'] = st.session_state['init_info']['metrics_json_file_path']
        st.session_state['title_json_file_path'] = st.session_state['init_info']['title_json_file_path']
        st.session_state['model'] = st.session_state['init_info']['model']
    if 'count_title' not in st.session_state:
        st.session_state['count_title'] = {}
    if 'uploaded_files_dict' not in st.session_state:
        st.session_state['uploaded_files_dict'] = {}
    if 'left_content_placeholder' not in st.session_state:
        st.session_state['left_content_placeholder'] = None
    return session_state