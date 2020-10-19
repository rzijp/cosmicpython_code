from dataclasses import dataclass


@dataclass()
class Orderline:
    sku: str
    quantity: int


@dataclass()
class Batch:
    id: str
    sku: str
    quantity: int

    def allocate(self, orderline: Orderline) -> bool:
        if orderline.quantity <= self.quantity:
            self.quantity = self.quantity - orderline.quantity
            return True
        else:
            return False
