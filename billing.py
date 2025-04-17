# billing.py

def calculate_bill(cart_items):
    subtotal = 0.0
    taxes = 0.0

    for item in cart_items:
        product = item.get('product', {})
        price = float(product.get('price', 0))  # Convert Decimal to float
        quantity = item.get('quantity', 0)
        category = product.get('category', '')

        item_total = price * quantity
        subtotal += item_total

        if category == "electronics":
            taxes += item_total * 0.18  # 18% GST

    discount = 0.1 * subtotal if subtotal > 1000 else 0
    total = subtotal - discount + taxes

    return {
        "items": cart_items,
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "taxes": round(taxes, 2),
        "total": round(total, 2)
    }
