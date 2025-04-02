import streamlit as st
from bs4 import BeautifulSoup
import re
import copy
## 自定义库↓
from Handel_pdf.Pdf_Handler import *
from Util import *
import traceback
import base64
import os



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

def main():
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

    # 创建两列布局，左边显示上传文档，右边显示a、b、c文档
    left_col, right_col = st.columns([1, 1])  # 调整列的宽度比例，左边更宽

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

    with right_col:
        st.markdown('<div class="right-header"><h2>内容展示区域</h2></div>', unsafe_allow_html=True)
        tab_selection2 = st.selectbox(
            "选择展示内容:",
            ("标题计数", "指标倒排索引", "PDF 预览")
        )

    # 上传文档部分（左列）
    with left_col:
        st.markdown('<div class="left-header"><h2>项目文件上传及原文展示</h2></div>', unsafe_allow_html=True)
        uploaded_files = st.file_uploader("上传Word文档", type=["pdf"], accept_multiple_files=True)
        # search_keyword = st.text_input("输入要搜索的关键词")
        # search_button = st.button("查找/查找下一个")
        left_content_placeholder = st.empty()

        # 处理文件上传逻辑
        if not uploaded_files:
            st.session_state['current_content'] = None
            st.session_state['left_doc_uploaded'] = False
            st.session_state['back_up_content'] = None
            st.session_state['uploaded_files_dict'] = {}
        if not st.session_state['current_content'] and uploaded_files:
            try:
                for uploaded_file in uploaded_files:
                    if uploaded_file.type == "application/pdf":
                        # 保存上传的文件到本地临时目录
                        file_path = os.path.join("temp_pdfs", uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        st.session_state['uploaded_files_dict'][uploaded_file.name] = {}
                        st.session_state['uploaded_files_dict'][uploaded_file.name]['file_path'] = file_path
                        st.session_state['uploaded_file_count'] += 1
                        print(f"开始处理第{st.session_state['uploaded_file_count']}个文件 {uploaded_file.name}！")
                        st.session_state['Handle_input_file_result'] = Handle_input_file(uploaded_file, st.session_state['metrics_json_file_path'],st.session_state['title_json_file_path'],st.session_state['model'])
                        result_dict = st.session_state['Handle_input_file_result']
                        print(f"第{st.session_state['uploaded_file_count']}个文件 {uploaded_file.name} 处理完毕！")
                        st.session_state['count_title'] = result_dict['title_count_dict']
                        st.session_state['uploaded_files_dict'][uploaded_file.name]['metrics_inverted_index'] = result_dict['metrics_inverted_index']
                        st.session_state['uploaded_files_dict'][uploaded_file.name]['metrics_with_class_dict'] = result_dict['metrics_with_class_dict']
                        st.session_state['left_doc_uploaded'] = True
                        st.session_state['current_content'] = result_dict['metrics_with_class_dict']
                        # 备份原始文档内容
                        st.session_state['back_up_content'] = copy.deepcopy(result_dict['metrics_with_class_dict'])
            except Exception as e:
                st.error(str(e))
                error_traceback = traceback.format_exc()
                # 打印错误堆栈信息到终端
                print(error_traceback)

        # if st.session_state['left_doc_uploaded']:
        with left_content_placeholder.container():
            show_json_content(st.session_state['current_content'])
            #st.components.v1.html(st.session_state['current_content'], height=600, scrolling=True)

        # 处理搜索按钮点击事件，只有在文档已上传后才生效
        # if st.session_state['left_doc_uploaded'] and search_button:
        #     if search_keyword != st.session_state.get('last_search_keyword', ''):
        #         # 关键词变化了，重新执行搜索
        #         st.session_state['last_search_keyword'] = search_keyword
        #         st.session_state['matches'] = []  # 清空上次的匹配项
        #         st.session_state['current_index'] = -1  # 重置为 - 1，表示没有匹配项
        #         st.session_state['current_content'] = st.session_state['back_up_content']  # 重置为原始文档内容
        #         # 执行新的搜索
        #         if search_keyword:
        #             print(f"开始搜索关键词：{search_keyword}")
        #             inverted_index = st.session_state['Handle_input_file_result']['All_metric_inverted_index']['data']
        #             # 获取搜索关键词对应的键值对
        #             search_result = inverted_index.get(search_keyword, {})
        #             # content = f"<div>{search_result}</div>"
        #             content = dict_to_html(search_result)
        #             soup_new_search = BeautifulSoup(content, 'html.parser')
        #             paragraphs = soup_new_search.find_all(['p', 'span', 'div', 'td', 'h3'])
        #             pattern = re.compile(re.escape(search_keyword), re.IGNORECASE)
        #             matches = []
        #             for idx, paragraph in enumerate(paragraphs):
        #                 if pattern.search(paragraph.get_text()):
        #                     highlighted_text = pattern.sub(lambda match: f"<mark style='background-color: yellow;'>{match.group(0)}</mark>",
        #                                                    paragraph.decode_contents())
        #                     paragraph.clear()
        #                     paragraph.append(BeautifulSoup(highlighted_text, 'html.parser'))
        #                     matches.append(paragraph)

        #             st.session_state['matches'] = matches
        #             st.session_state['current_index'] = 0  # 重新开始从第一个匹配项
        #             st.session_state['current_content'] = str(soup_new_search)  # 更新文档内容为高亮后的内容
        #             if matches:
        #                 for idx, paragraph in enumerate(matches):
        #                     if idx == st.session_state['current_index']:
        #                         paragraph['id'] = 'current_match'
        #                         paragraph['style'] = 'background-color: orange;'  # 当前匹配项用橙色高亮
        #                     else:
        #                         paragraph['id'] = ''
        #                         paragraph['style'] = 'background-color: yellow;'  # 其他匹配项用黄色高亮
        #                 # 保存高亮后的内容
        #                 st.session_state['current_content'] = str(soup_new_search)
        #     elif search_keyword == st.session_state.get('last_search_keyword', ''):
        #         # 关键词没有变化，查找下一个匹配项
        #         if st.session_state['matches']:
        #             # 只有在有匹配项时才进行查找
        #             st.session_state['current_index'] = (st.session_state['current_index'] + 1) % len(st.session_state['matches'])
        #             soup_repeat = BeautifulSoup(st.session_state['current_content'], 'html.parser')
        #             paragraphs = soup_repeat.find_all(['p', 'span', 'div', 'td', 'h3'])
        #             pattern = re.compile(re.escape(search_keyword), re.IGNORECASE)
        #             # 更新高亮颜色
        #             idx = -1
        #             for paragraph in paragraphs:
        #                 # 对当前匹配项和上一项进行样式更新
        #                 if pattern.search(paragraph.get_text()):
        #                     idx += 1
        #                     if idx == st.session_state['current_index']:
        #                         # 当前匹配项用橙色高亮
        #                         paragraph['id'] = 'current_match'
        #                         paragraph['style'] = 'background-color: orange;'
        #                     else:
        #                         # 其他匹配项用黄色高亮
        #                         paragraph['id'] = ''
        #                         paragraph['style'] = 'background-color: yellow;'

        #             # 保存高亮后的内容
        #             st.session_state['current_content'] = str(soup_repeat)

        #     # 在页面加载时滚动到当前匹配的结果
        #     # scroll_script = """
        #     # <script>
        #     #     document.addEventListener('DOMContentLoaded', function() {
        #     #         var element = document.getElementById('current_match');
        #     #         if(element) {
        #     #             element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        #     #         }
        #     #     });
        #     # </script>
        #     # """
        #     with left_content_placeholder.container():
        #         show_json_content(st.session_state['current_content'])
        #         # st.components.v1.html(st.session_state['current_content'] + scroll_script, height=600, scrolling=True)

    with right_col:
        right_content_placeholder = st.empty()
        if st.session_state['left_doc_uploaded']:
            if tab_selection2 == "标题计数":
                st.session_state["right_doc_content"] = st.session_state['count_title']
            elif tab_selection2 == "指标倒排索引":
                st.session_state["right_doc_content"] = st.session_state['Handle_input_file_result']['All_metric_inverted_index']
            elif tab_selection2 == "PDF 预览":
                if st.session_state['uploaded_files_dict']:
                    selected_file = st.selectbox("选择要预览的 PDF 文件", list(st.session_state['uploaded_files_dict'].keys()))
                    file_path = st.session_state['uploaded_files_dict'][selected_file]['file_path']
                    st_display_pdf(file_path)
                    st.session_state['current_content'] = st.session_state['uploaded_files_dict'][selected_file]['metrics_with_class_dict']
                    with left_content_placeholder.container():
                        show_json_content(st.session_state['current_content'])
        else:
            st.session_state['right_doc_content'] = ""
            right_content_placeholder.empty()
        if 'right_selected_doc' not in st.session_state:
            st.session_state['right_selected_doc'] = None

        if st.session_state["right_doc_content"] and tab_selection2 != "PDF 预览":
            with right_content_placeholder.container():
                show_json_content(st.session_state['right_doc_content'])
                # try:
                #     json_content = json.dumps(st.session_state["right_doc_content"], indent=4, ensure_ascii=False)
                #     st.code(json_content, language="json")
                # except (TypeError, ValueError):
                #         # 如果不是 JSON 格式，按普通文本显示
                #         st.markdown(f"""
                #         <div style="height: 750px; overflow-y: scroll; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
                #             {st.session_state["right_doc_content"]}
                #         </div>
                #         """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()