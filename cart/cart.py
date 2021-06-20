from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item, quantity=1, override_quantity=False):
        """
        Add a product to a cart or update its quantity
        """
        if str(item.id) not in self.cart.keys():
            self.cart[str(item.id)] = {'quantity': 0, 'price': str(item.price)}
        if override_quantity:
            self.cart[str(item.id)]['quantity'] = quantity
        else:
            self.cart[str(item.id)]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as modified to make sure it gets saved
        self.session.modified = True

    def remove(self, item):
        if str(item.id) in self.cart.keys():
            del self.cart[str(item.id)]
            self.save()

    def get_total_price(self):
        return sum(
            item['quantity'] * Decimal(item['price']) for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        yield {
            "total_price": Decimal,
            "price": str,
            "quantity": int,
            "product": Product }
        """
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        """
        sum all items quantity in cart
        """
        return sum(item['quantity'] for item in self.cart.values())
