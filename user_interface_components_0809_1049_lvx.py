# 代码生成时间: 2025-08-09 10:49:50
# 用户界面组件库
# 使用Bottle框架实现
# 扩展功能模块
# 遵循Python最佳实践和代码规范

from bottle import route, run, template, static_file, error
# NOTE: 重要实现细节
import os

# 定义基本路径
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(BASE_PATH, 'static')
TEMPLATE_PATH = os.path.join(BASE_PATH, 'views')

# 定义路由
@route('/')
def index():
    # 首页显示
    return template('index')

@route('/static/<filename:path>')
def serve_static(filename):
    # 静态文件服务
    return static_file(filename, root=STATIC_PATH)

@route('/component/<name>')
def show_component(name):
    # 显示组件
    try:
        # 根据组件名称返回对应的HTML模板
        return template('components/' + name)
    except template.TemplateError:
        # 模板不存在时返回404错误
        return error(404, 'Component not found')

# 定义错误处理
@error(404)
def error404(error):
    return template('404')
# 扩展功能模块

# 启动服务器
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
