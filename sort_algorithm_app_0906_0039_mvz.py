# 代码生成时间: 2025-09-06 00:39:27
# sort_algorithm_app.py

# 导入Bottle框架
from bottle import route, run
import json

# 定义排序算法
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)

# 路由定义，处理排序请求
@route('/sort', method='POST')
def sort_request():
    try:
        # 解析请求体中的JSON数据
        request_data = json.loads(request.body.read())
        # 获取要排序的数组
        arr = request_data.get('array')
        # 检查数组是否有效
        if not isinstance(arr, list) or not all(isinstance(x, (int, float)) for x in arr):
            return json.dumps({'error': 'Invalid array or data type'})
        # 执行排序算法
        sorted_arr = quick_sort(arr)
        # 返回排序结果
        return json.dumps({'sorted_array': sorted_arr})
    except Exception as e:
        # 错误处理
        return json.dumps({'error': str(e)})

# 运行Bottle服务器
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
