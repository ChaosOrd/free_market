from math import copysign


class Exchange(object):

    def __init__(self):
        self.__book = []
        self.__order_sequence_number = 0

    def place_order(self, order):
        self.__book.append(BookEntry(self.__order_sequence_number, order))
        self.__order_sequence_number += 1

        self.__sort_book()
        self.__fill_orders_if_needed()

    def __sort_book(self):
        def get_order_entry_key(order_entry):
            order = order_entry.order
            return copysign(order.price, order.quantity)
        self.__book = sorted(self.__book, key=get_order_entry_key)

    def __fill_orders_if_needed(self):
        for idx in range(len(self.__book)-1):
            self.__fill_orders_if_crossing(self.__book[idx],
                                           self.__book[idx+1])

    def __fill_orders_if_crossing(self, first_entry, second_entry):
        first_order = first_entry.order
        second_order = second_entry.order
        if first_order.price >= second_order.price:
            self.__fill_orders(first_entry, second_entry)

    def __fill_orders(self, first_entry, second_entry):
        first_order = first_entry.order
        second_order = second_entry.order

        price = self.__calc_crossing_entries_price(first_entry, second_entry)
        abs_quantity = self.__calc_crossing_orders_absolute_qty(first_order,
                                                                second_order)
        first_order.sender.on_order_filled(
            order=first_order, price=price,
            quantity=copysign(abs_quantity, first_order.quantity))
        second_order.sender.on_order_filled(
            order=second_order, price=price,
            quantity=copysign(abs_quantity, second_order.quantity))

    def __calc_crossing_orders_absolute_qty(self, first_order, second_order):
        return min(abs(first_order.quantity), abs(second_order.quantity))

    def __calc_crossing_entries_price(self, first_entry, second_entry):
        if (first_entry.sequence < second_entry.sequence):
            return first_entry.order.price
        else:
            return second_entry.order.price


class BookEntry(object):

    def __init__(self, sequence, order):
        self.__sequence = sequence
        self.__order = order

    @property
    def sequence(self):
        return self.__sequence

    @property
    def order(self):
        return self.__order


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
