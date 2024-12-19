def handle_cart(cart):
    total_price, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_price += c['quantity'] * c['price']

    return {
       "total_price": total_price,
       "total_quantity": total_quantity
    }
