# 代码生成时间: 2025-08-20 18:43:45
from bottle import route, run, request, response, template

# 简单的购物车数据结构
SHOPPING_CART = {}

# 初始化购物车路由
@route('/shopping_cart')
def shopping_cart():
    """
    显示当前用户的购物车内容。
    如果用户没有购物车，返回一个空购物车的消息。
    """
    session_id = request.get_cookie('session_id')
    if session_id not in SHOPPING_CART:
        return template("""
        <html><body>
        <h2>Your shopping cart is empty!</h2>
        </body></html>
        """)
    return template("""
    <html><body>
    <h2>Your shopping cart:</h2>
    <ul>%for item in items:
        <li>{{item['name']}} - {{item['quantity']}}</li>
    %end
    </ul>
    </body></html>
    """, items=SHOPPING_CART[session_id])

# 添加商品到购物车路由
@route('/add_to_cart/<session_id>/<product_name>/<quantity>')
def add_to_cart(session_id, product_name, quantity):
    """
    添加商品到用户的购物车。
    如果商品已经存在，则增加数量；否则，添加新商品。
    """
    try:
        quantity = int(quantity)
    except ValueError:
        response.status = 400
        return 'Invalid quantity'
    
    if session_id not in SHOPPING_CART:
        SHOPPING_CART[session_id] = {}
    
    if product_name in SHOPPING_CART[session_id]:
        SHOPPING_CART[session_id][product_name]['quantity'] += quantity
    else:
        SHOPPING_CART[session_id][product_name] = {'name': product_name, 'quantity': quantity}
    
    response.set_cookie('session_id', session_id)
    return 'Item added to cart successfully'

# 主函数，启动Bottle服务器
def main():
    """
    启动Bottle服务器，监听8080端口。
    """
    run(host='localhost', port=8080)

if __name__ == '__main__':
    main()
