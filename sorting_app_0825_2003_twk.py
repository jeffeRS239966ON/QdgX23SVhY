# 代码生成时间: 2025-08-25 20:03:41
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bottle web framework for python
from bottle import Bottle, route, run, request, response
import json

# 创建 Bottle 应用
app = Bottle()

# 定义一个简单的排序算法: 冒泡排序
def bubble_sort(arr):
    n = len(arr)
    # 遍历所有数组元素
    for i in range(n):
        # 最后i个元素已经是排好序的了，不需要再比较
        for j in range(0, n-i-1):
            # 遍历数组从0到n-i-1
            # 交换如果发现元素e[j]比e[j+1]大，则交换之
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# API 路由: 排序
@route('/sort', method='POST')
def sort_numbers():
    try:
        # 获取 JSON 数据
        data = request.json
        if not data:
            raise ValueError("No data provided")
        arr = data.get('numbers')
        # 检查数据类型
        if not isinstance(arr, list) or not all(isinstance(item, (int, float)) for item in arr):
            raise ValueError("Invalid data format. Expecting a list of numbers.")
        # 进行排序
        sorted_arr = bubble_sort(arr)
        # 设置响应头为 JSON
        response.content_type = 'application/json'
        # 返回排序结果
        return json.dumps({'sorted_numbers': sorted_arr})
    except Exception as e:
        # 设置响应头为 JSON
        response.content_type = 'application/json'
        # 返回错误信息
        return json.dumps({'error': str(e)})

# 设置主机和端口
host = 'localhost'
port = 8080

# 运行 Bottle 应用
if __name__ == '__main__':
    run(app, host=host, port=port, debug=True)
