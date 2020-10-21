from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set


class OutOfStock(Exception):
    pass


@dataclass(frozen=True)
class Orderline:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(
        self, id: str, sku: str, purchased_quantity: int, eta: Optional[date] = None
    ) -> None:
        self.id = id
        self.sku = sku
        self.purchased_quantity = purchased_quantity
        self.eta = eta
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

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __eq__(self, other):
        if not(isinstance(other, type(self))):
            return False
        return self.id == other.id


def allocate(orderline: Orderline, batches: List[Batch]) -> str:
    try:
        first_available_batch = next(
            b for b in sorted(batches) if b.can_allocate(orderline)
        )
    except StopIteration:
        raise OutOfStock(
            f"No stock available for {orderline.quantity} units of {orderline.sku}"
        )
    first_available_batch.allocate(orderline)
    return first_available_batch.id
