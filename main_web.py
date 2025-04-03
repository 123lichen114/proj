import streamlit as st
from web_page.left_column import left_column_content
from web_page.right_column import right_column_content
from web_page.web_init_config import init_web
def main():
    st.session_state = init_web(st.session_state)
    # 创建两列布局，左边显示上传文档，右边显示a、b、c文档
    left_col, right_col = st.columns([1, 1])  # 调整列的宽度比例，左边更宽    
    with left_col:
        st.session_state = left_column_content(st.session_state)
    with right_col:
        st.session_state = right_column_content(st.session_state)

if __name__ == "__main__":
    main()