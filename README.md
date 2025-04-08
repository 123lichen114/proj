## 招标文件解析助手

执行方式

```
cd path/to/proj
conda activate zhaobiao
./run.sh
```

项目结构功能介绍

- main_web.py 主程序

* web_page:网页设置和逻辑组织，Util.py 是一些杂项功能函数
* Handel_pdf:处理pdf文件，inverted_index.py用来生成一些倒排索引，read_pdf.py完成pdf文档转换到模型输入文本这一步，read_content_to_target_content.py将extract_text_from_pdf的结果输入给模型。Pdf_Handler.py是主接口，在web_page中被调用。
* data保存了一些文件，但是实际上没有用到，文档是用户本地上传的。
