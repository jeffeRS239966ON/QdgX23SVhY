# 代码生成时间: 2025-08-01 22:17:02
# 导入 Bottle 框架
from bottle import route, run, template, static_file, redirect

# 定义全局变量存储组件数据
component_library = {
    "buttons": "<button>{{text}}</button>",
    "inputs": "<input type='text' placeholder='{{placeholder}}' />",
    "labels": "<label>{{text}}</label>"
}

# 路由：首页
@route('/')
def home():
    # 渲染首页模板
    return template("""
    <h1>Welcome to User Interface Components Library</h1>
    <p>Select a component to view:</p>
    <ul>
        {{for component in components}}
            <li><a href='/component/{{component}}'>{{component}}</a></li>
        {{endfor}}
    </ul>
    """, components=list(component_library.keys()))

# 路由：组件详情页
@route('/component/<component_name>')
def component_detail(component_name):
    # 检查组件是否存在
    if component_name not in component_library:
        return template("<h1>Component not found</h1>")
    # 返回组件的详情页面
    return template("""
    <h2>Component: {{component_name}}</h2>
    <p>{{code}}</p>
    """, component_name=component_name, code=component_library[component_name])

# 路由：静态文件服务（CSS, JS等）
@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='static')

# 路由：重定向到首页
@route('/redirect')
def redirect_to_home():
    redirect('/')

# 主程序 - 启动 Bottle 服务器
if __name__ == '__main__':
    run(host='localhost', port=8080)
