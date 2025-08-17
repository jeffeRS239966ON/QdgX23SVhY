# 代码生成时间: 2025-08-17 22:48:06
from bottle import route, run, request, response, abort

# 数据库模拟
inventory = {}

# 列出所有库存项
@route('/inventory', method='GET')
def list_inventory():
    response.content_type = 'application/json'
    return {"data": inventory}

# 获取单个库存项
@route('/inventory/<item_id:int>', method='GET')
def get_inventory_item(item_id):
    if item_id in inventory:
        response.content_type = 'application/json'
        return {"data": inventory[item_id]}
    else:
        abort(404, "Item not found")

# 添加新的库存项
@route('/inventory', method='POST')
def add_inventory_item():
    try:
        data = request.json
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        if item_id is None or quantity is None:
            abort(400, "Missing item_id or quantity")
        elif item_id in inventory:
            abort(409, "Item already exists")
        else:
            inventory[item_id] = quantity
            response.content_type = 'application/json'
            return {"message": "Item added", "item": data}
    except Exception as e:
        abort(500, "Internal Server Error: " + str(e))

# 更新库存项
@route('/inventory/<item_id:int>', method='PUT')
def update_inventory_item(item_id):
    try:
        data = request.json
        new_quantity = data.get('quantity')
        if new_quantity is None:
            abort(400, "Missing quantity")
        elif item_id not in inventory:
            abort(404, "Item not found")
        else:
            inventory[item_id] = new_quantity
            response.content_type = 'application/json'
            return {"message": "Item updated", "item": data}
    except Exception as e:
        abort(500, "Internal Server Error: " + str(e))

# 删除库存项
@route('/inventory/<item_id:int>', method='DELETE')
def delete_inventory_item(item_id):
    if item_id in inventory:
        del inventory[item_id]
        response.content_type = 'application/json'
        return {"message": "Item deleted"}
    else:
        abort(404, "Item not found")

# 运行服务器
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)