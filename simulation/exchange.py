class Exchange(object):
    pass


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
