# 代码生成时间: 2025-08-09 00:00:23
#!/usr/bin/env python

"""
Excel表格自动生成器

这个程序使用Python和Bottle框架来生成Excel表格。
它提供了一个简单的HTTP接口来接收数据，并将其转换为Excel文件。
"""

from bottle import Bottle, response, request
import pandas as pd
from io import BytesIO

# 初始化Bottle应用
app = Bottle()

"""
生成Excel文件

这个函数接受一个JSON对象，包含要生成Excel文件的数据。
它将数据转换为Pandas DataFrame，然后保存为Excel文件。
"""
@app.route('/generate', method='POST')
def generate_excel():
    try:
        # 从请求体中获取JSON数据
        data = request.json
        # 检查数据是否有效
        if not data or 'data' not in data:
            response.status = 400
            return {"error": "Invalid data"}

        # 将数据转换为Pandas DataFrame
        df = pd.DataFrame(data['data'])

        # 创建一个BytesIO对象来保存Excel文件
        excel_buffer = BytesIO()

        # 将DataFrame保存为Excel文件
        df.to_excel(excel_buffer, index=False)

        # 将文件内容设置为响应体
        excel_buffer.seek(0)
        response.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.setHeader('Content-Disposition', 'attachment; filename=generated_excel.xlsx')
        return excel_buffer.read()

    except Exception as e:
        # 处理任何异常
        response.status = 500
        return {"error": str(e)}

# 启动Bottle应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)