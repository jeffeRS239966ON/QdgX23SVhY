# 代码生成时间: 2025-08-19 21:44:41
# 文件夹结构整理器
# 使用Bottle框架创建的简单Web服务
# 用于整理指定文件夹的结构

from bottle import Bottle, request, response, run
import os
import shutil
from pathlib import Path

# 初始化Bottle应用
app = Bottle()

# 定义配置常量
DEFAULT_SORT_DIR = 'asc'  # 默认排序方向
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif'}  # 允许的文件扩展名

# 错误处理装饰器
def error_handler(error):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error as e:
                response.status = 400
                return {'error': str(e)}
        return wrapper
    return decorator

# 文件夹整理API
@app.route('/organize', method='POST')
@error_handler(FileNotFoundError)
def organize_folder():
    # 获取请求数据
    data = request.json
    folder_path = data.get('folder_path')
    sort_order = data.get('sort_order', DEFAULT_SORT_DIR)  # 获取排序方式，默认为升序

    # 验证文件夹路径
    if not folder_path or not Path(folder_path).is_dir():
        response.status = 400
        return {'error': 'Invalid folder path'}

    # 开始整理文件夹
    try:
        organize_directory(folder_path, sort_order)
        return {'message': 'Folder organized successfully'}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# 整理文件夹的函数
def organize_directory(folder_path, sort_order):
    """
    整理指定文件夹，将文件按扩展名分类到子文件夹中。
    :param folder_path: 需要整理的文件夹路径
    :param sort_order: 排序方式，'asc'升序或'desc'降序
    """
    # 遍历文件夹中的所有文件和子文件夹
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        # 如果是文件，则根据扩展名移动到对应的子文件夹
        if os.path.isfile(item_path):
            file_ext = Path(item_path).suffix
            if file_ext in ALLOWED_EXTENSIONS:
                dest_folder = os.path.join(folder_path, file_ext[1:])  # 创建以扩展名命名的子文件夹
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(item_path, os.path.join(dest_folder, item))
        # 如果是文件夹，则递归整理
        elif os.path.isdir(item_path):
            organize_directory(item_path, sort_order)

# 运行应用
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)