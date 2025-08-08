# 代码生成时间: 2025-08-08 08:02:17
from bottle import route, run, template, static_file

# 全局变量定义页面标题和静态文件目录
PAGE_TITLE = "Responsive Layout with Bottle"
STATIC_FILES_DIR = "./static"

# 路由处理根路径，返回一个响应式布局的HTML页面
@route("/")
def home():
    # 返回使用模板渲染的HTML页面
    return template("index", title=PAGE_TITLE)

# 路由处理静态文件请求
@route("/static/<filename:path>")
def send_static(filename):
    # 返回静态文件
    return static_file(filename, root=STATIC_FILES_DIR)

# 启动Bottle服务器，监听localhost的8080端口
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)

# 模板文件index.tpl
# {% extends "base.tpl" %}
# {% block content %}
#     <h1>{{title}}</h1>
#     <p>This is a responsive layout demo.</p>
#     <p>Resize your browser to see the responsive design in action.</p>
# {% endblock %}

# 模板文件base.tpl
# <!DOCTYPE html>
# <html lang="en">\#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>{{title}}</title>
#         <link rel="stylesheet" href="/static/style.css">
#         <style>
#             /* CSS styles for responsive layout */
#             @media (max-width: 600px) {
#                 body {
#                     background-color: lightblue;
#                 }
#             }
#             @media (min-width: 601px) and (max-width: 1200px) {
#                 body {
#                     background-color: lightgreen;
#                 }
#             }
#             @media (min-width: 1201px) {
#                 body {
#                     background-color: lightcoral;
#                 }
#             }
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             {% block content %}{% endblock %}
#         </div>
#     </body>
# </html>