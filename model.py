from dataclasses import dataclass


@dataclass()
class Orderline:
    sku: str
    quantity: int


@dataclass()
class Batch:
    id: str
    sku: str
    available_quantity: int

    def can_allocate(self, orderline: Orderline) -> bool:
        return (
            self.sku == orderline.sku and orderline.quantity <= self.available_quantity
        )

    def allocate(self, orderline: Orderline) -> None:
        if self.can_allocate(orderline):
            self.available_quantity = self.available_quantity - orderline.quantity
