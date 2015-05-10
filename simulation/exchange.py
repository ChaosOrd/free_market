from math import copysign


class Exchange(object):

    def __init__(self):
        self.__book = []
        self.__order_sequence_number = 0

    def place_order(self, order):
        self.__book.append((self.__order_sequence_number, order))
        self.__order_sequence_number += 1

        self.__sort_book()
        self.__fill_orders_if_needed()

    def __sort_book(self):
        def get_order_entry_key(order_entry):
            order = order_entry[1]
            return copysign(order.price, order.quantity)
        self.__book = sorted(self.__book, key=get_order_entry_key)

    def __fill_orders_if_needed(self):
        for idx in range(len(self.__book)-1):
            self.__fill_orders_if_crossing(self.__book[idx],
                                           self.__book[idx+1])

    def __fill_orders_if_crossing(self, first_entry, second_entry):
        first_sequence, first_order = first_entry
        second_sequence, second_order = second_entry
        if (first_order.price >= second_order.price):
            price = first_order.price if second_sequence > first_sequence \
                else second_order.price
            first_order.sender.on_order_filled(order=first_order, price=price,
                                               quantity=first_order.quantity)
            second_order.sender.on_order_filled(order=second_order, price=price,
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
