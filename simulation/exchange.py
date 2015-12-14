from enum import Enum
from math import copysign


class Order(object):
    def __init__(self, resource, price, quantity):
        self._resource = resource
        self._price = price
        self._quantity = quantity

    @property
    def resource(self):
        return self._resource

    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def side(self):
        if self.quantity > 0:
            return OrderSide.Buy

        if self.quantity < 0:
            return OrderSide.Sell

        return None


class Exchange(object):
    def __init__(self):
        self.__book = {}
        self.__order_sequence_number = 0

    def place_order(self, order, sender):
        order_resource = order.resource
        if order_resource not in self.__book:
            self.__book[order_resource] = []

        book_resource = self.__book[order_resource]

        book_resource.append(BookEntry(self.__order_sequence_number, order, sender))
        self.__order_sequence_number += 1

        self.__sort_book()
        self.__fill_orders_if_needed()

        for order_entry in book_resource:
            order = order_entry.order
            if order.quantity == 0:
                self.__book[order_resource].remove(order_entry)

    def get_best_sell(self, resource: str) -> Order:
        def comparison_criteria(order1, order2):
            return order1.price < order2.price

        def filtering_criteria(order):
            return order.side == OrderSide.Sell

        return self.__find_order(resource, filtering_criteria, comparison_criteria)

    def get_best_buy(self, resource: str):
        def comparison_criteria(order1, order2):
            return order1.price > order2.price

        def filtering_criteria(order):
            return order.side == OrderSide.Buy

        return self.__find_order(resource, filtering_criteria, comparison_criteria)

    @property
    def book_size(self):
        return len(self.__book)

    def __find_order(self, resource, filtering_criteria, comparison_criteria):
        if resource not in self.__book:
            return None

        max_comparison_order = None
        for book_entry in self.__book[resource]:
            order = book_entry.order

            if filtering_criteria(order):
                if max_comparison_order is None or comparison_criteria(order, max_comparison_order):
                    max_comparison_order = order

        return max_comparison_order

    def __sort_book(self):
        def get_order_entry_key(order_entry):
            order = order_entry.order
            return copysign(order.price, order.quantity)

        for book_resource in self.__book:
            self.__book[book_resource] = sorted(self.__book[book_resource], key=get_order_entry_key)

    def __fill_orders_if_needed(self):
        for resource in self.__book:
            book_resource = self.__book[resource]
            for idx in range(len(book_resource) - 1):
                self.__fill_orders_if_crossing(book_resource[idx],
                                               book_resource[idx + 1])

    def __fill_orders_if_crossing(self, first_entry, second_entry):
        first_order = first_entry.order
        second_order = second_entry.order
        if first_order.side != second_order.side and first_order.price <= second_order.price:
            self.__fill_orders(first_entry, second_entry)

    def __fill_orders(self, first_entry, second_entry):
        first_order = first_entry.order
        second_order = second_entry.order

        price = self.__calc_crossing_entries_price(first_entry, second_entry)
        abs_quantity = self.__calc_crossing_orders_absolute_qty(first_order,
                                                                second_order)

        first_order_quantity = copysign(abs_quantity, first_order.quantity)
        first_entry.sender.on_order_filled(order=first_order, price=price, quantity=first_order_quantity)
        first_order.quantity -= first_order_quantity

        second_order_quantity = copysign(abs_quantity, second_order.quantity)
        second_entry.sender.on_order_filled(order=second_order, price=price, quantity=second_order_quantity)
        second_order.quantity -= second_order_quantity

    @staticmethod
    def __calc_crossing_orders_absolute_qty(first_order, second_order):
        return min(abs(first_order.quantity), abs(second_order.quantity))

    @staticmethod
    def __calc_crossing_entries_price(first_entry, second_entry):
        if first_entry.sequence < second_entry.sequence:
            return first_entry.order.price
        else:
            return second_entry.order.price

    def get_orders_sent_by(self, sender):
        sent_orders = []
        for book_resource in self.__book:
            for order_entry in self.__book[book_resource]:
                if order_entry.sender == sender:
                    sent_orders.append(order_entry.order)
        return sent_orders

    def get_number_of_placed_orders(self, standard_resource):
        if standard_resource not in self.__book:
            return 0

        return len(self.__book[standard_resource])


class BookEntry(object):
    def __init__(self, sequence, order, sender):
        self.__sequence = sequence
        self.__order = order
        self.__sender = sender

    @property
    def sequence(self):
        return self.__sequence

    @property
    def order(self):
        return self.__order

    @property
    def sender(self):
        return self.__sender

    def __repr__(self):
        return "Sequence: {}, Order: {}".format(self.sequence, self.order)


class OrderSide(Enum):
    Buy = 0
    Sell = 1
