from dataclasses import dataclass
from typing import Set


@dataclass(frozen=True)
class Orderline:
    sku: str
    quantity: int


class Batch:
    def __init__(self, id: str, sku: str, purchased_quantity: int) -> None:
        self.id = id
        self.sku = sku
        self.purchased_quantity = purchased_quantity
        self._orderlines = set()  # type: Set[Orderline]

    def can_allocate(self, orderline: Orderline) -> bool:
        return (
            self.sku == orderline.sku and orderline.quantity <= self.available_quantity
        )

    def allocate(self, orderline: Orderline) -> None:
        if self.can_allocate(orderline):
            self._orderlines.add(orderline)

    def deallocate(self, orderline: Orderline) -> None:
        if orderline in self._orderlines:
            self._orderlines.remove(orderline)

    @property
    def allocated_quantity(self):
        return sum([line.quantity for line in self._orderlines])

    @property
    def available_quantity(self):
        return self.purchased_quantity - self.allocated_quantity
