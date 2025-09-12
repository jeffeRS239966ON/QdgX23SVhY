# 代码生成时间: 2025-09-12 12:46:40
# api_response_formatter.py
"""
API响应格式化工具，使用Bottle框架。
提供统一的API响应格式，包括错误处理和数据封装。
"""
from bottle import Bottle, request, response
import json

app = Bottle()

# 统一响应格式
class ApiResponse:
    def __init__(self, data=None, message='', status=200, errors=None):
        self.data = data
        self.message = message
        self.status = status
        self.errors = errors if errors else []

    def to_dict(self):
        return {
            "code": self.status,
            "message": self.message,
            "data": self.data,
            "errors": self.errors
        }

# 设置JSON响应格式
@app.error(400)
@app.error(404)
@app.error(500)
def error_handler(error):
    response.status = error.status_code
    response.content_type = 'application/json'
    api_response = ApiResponse(
        message=error.body,
        status=error.status_code
    )
    return api_response.to_dict()

# API响应格式化工具
def api_response(data=None, message='Success', status=200, errors=None):
    api_response = ApiResponse(data, message, status, errors)
    return json.dumps(api_response.to_dict(), ensure_ascii=False)

# 示例API
@app.route('/api/example', method='GET')
def example_api():
    try:
        # 模拟业务逻辑
        data = {"name": "John", "age": 30}
        return api_response(data)
    except Exception as e:
        # 错误处理
        return api_response(message=str(e), status=500)

# 运行Bottle应用
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)