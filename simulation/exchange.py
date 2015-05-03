from math import copysign


class Exchange(object):

    def __init__(self):
        self.book = []

    def place_order(self, order):
        self.book.append(order)

        self.book = sorted(self.book, key=lambda o: copysign(o.price, o.quantity))
        self.__fill_orders_if_needed()

    def __fill_orders_if_needed(self):
        for idx in range(len(self.book)-1):
            first_order = self.book[idx]
            second_order = self.book[idx+1]
            if (first_order.price >= second_order.price):
                first_order.sender.on_order_filled(order=first_order,
                                                   price=second_order.price,
                                                   quantity=first_order.quantity)
                second_order.sender.on_order_filled(order=second_order,
                                                    price=second_order.price,
                                                    quantity=second_order.quantity)


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
