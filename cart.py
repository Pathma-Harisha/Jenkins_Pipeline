# cart.py

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        for item in self.items:
            if item['product']['id'] == product['id']:
                item['quantity'] += quantity
                return
        self.items.append({'product': product, 'quantity': quantity})

    def remove_item(self, product_id):
        self.items = [item for item in self.items if item['product']['id'] != product_id]

    def update_quantity(self, product_id, quantity):
        for item in self.items:
            if item['product']['id'] == product_id:
                item['quantity'] = quantity

    def clear_cart(self):
        self.items = []

    def get_items(self):
        return self.items
