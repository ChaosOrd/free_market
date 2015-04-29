class Exchange(object):

    def place_order(self, order):
        order.sender.on_order_filled(order=order,
                                     price=order.price,
                                     quantity=order.quantity)


class Order(object):

    def __init__(self, sender, resource, price, quantity):
        self._resource = resource
        self._price = price
        self._quantity = quantity
        self._sender = sender

    @property
    def resource(self):
        return self._resource

    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity

    @property
    def sender(self):
        return self._sender
