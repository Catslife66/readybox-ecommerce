class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart


    def update_item(self, item, serving, quantity):
        item_id = str(item.id)
        serving_id = str(serving.id)
        if item_id in self.cart:
            self.cart[item_id]['quantity'] = quantity
            if self.cart[item_id]['quantity'] <= 0:
                del self.cart[item_id]
        else:
            self.cart[item_id] = {
                'serving_id': serving_id,
                'quantity': quantity
            }
        self.save()


    def remove_item(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
        self.save()


    def save(self):
        # Save the cart data to the session
        self.session['cart'] = self.cart
        self.session.modified = True