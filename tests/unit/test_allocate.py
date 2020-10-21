from datetime import date, timedelta
from typing import Tuple

import pytest

from allocation.domain.model import Batch, Orderline, OutOfStock, allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def create_batch_and_orderline(
    sku: str, batch_quantity: int, orderline_quantity: int
) -> Tuple[Batch, Orderline]:
    batch = Batch(id="123", sku=sku, purchased_quantity=batch_quantity)
    orderline = Orderline(order_id="789", sku=sku, quantity=orderline_quantity)
    return batch, orderline


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_orderline = create_batch_and_orderline("RED CHAIR", 20, 2)
    assert large_batch.can_allocate(small_orderline)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    large_batch, small_orderline = create_batch_and_orderline("RED CHAIR", 20, 2)
    large_batch.allocate(small_orderline)
    assert large_batch.available_quantity == 18


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_orderline = create_batch_and_orderline("RED CHAIR", 2, 20)
    assert small_batch.can_allocate(large_orderline) is False


def test_can_allocate_if_available_equal_to_required():
    batch, same_size_orderline = create_batch_and_orderline("RED CHAIR", 10, 10)
    batch.allocate(same_size_orderline)
    assert batch.available_quantity == 0


def test_cannot_allocate_different_SKU():
    batch = Batch("123", sku="GREEN TABLE", purchased_quantity=10)
    wrong_sku_orderline = Orderline(order_id="789", sku="RED CHAIR", quantity=2)
    assert batch.can_allocate(wrong_sku_orderline) is False


def test_cannot_deallocate_unallocated_orderline():
    batch, allocated_orderline = create_batch_and_orderline("GREEN TABLE", 10, 2)
    unallocated_orderline = Orderline(order_id="789", sku="BLUE SOFA", quantity=1)
    batch.allocate(allocated_orderline)
    assert batch.available_quantity == 8
    batch.deallocate(unallocated_orderline)
    assert batch.available_quantity == 8


def test_prefers_warehouse_batches_to_shipments():
    batch_in_stock = Batch(id="1", sku="BLACK DESK", purchased_quantity=2)
    batch_in_shipment = Batch(id="2", sku="BLACK DESK", purchased_quantity=2, eta=today)
    orderline = Orderline(order_id="789", sku="BLACK DESK", quantity=1)
    allocate(orderline, [batch_in_shipment, batch_in_stock])
    assert batch_in_stock.available_quantity == 1
    assert batch_in_shipment.available_quantity == 2


def test_prefers_earlier_batches():
    batch_early = Batch(id="1", sku="BLACK DESK", purchased_quantity=2, eta=tomorrow)
    batch_late = Batch(id="2", sku="BLACK DESK", purchased_quantity=2, eta=later)
    orderline = Orderline(order_id="789", sku="BLACK DESK", quantity=1)
    allocate(orderline, [batch_late, batch_early])
    assert batch_early.available_quantity == 1
    assert batch_late.available_quantity == 2


def test_ignores_too_small_batch():
    batch_in_stock_but_too_small = Batch(id="1", sku="BLACK DESK", purchased_quantity=1)
    batch_late = Batch(id="2", sku="BLACK DESK", purchased_quantity=2, eta=later)
    orderline = Orderline(order_id="789", sku="BLACK DESK", quantity=2)
    allocate(orderline, [batch_in_stock_but_too_small, batch_late])
    assert batch_in_stock_but_too_small.available_quantity == 1
    assert batch_late.available_quantity == 0


def test_out_of_stock():
    batch_1 = Batch(id="1", sku="MEMORY", purchased_quantity=1)
    batch_2 = Batch(id="2", sku="MEMORY", purchased_quantity=2)
    orderline = Orderline(order_id="789", sku="MEMORY", quantity=3)
    with pytest.raises(OutOfStock):
        allocate(orderline, [batch_1, batch_2])


def test_returns_allocated_batch_ref():
    batch_1 = Batch(id="1", sku="MEMORY", purchased_quantity=2, eta=today)
    batch_2 = Batch(id="2", sku="MEMORY", purchased_quantity=2, eta=tomorrow)
    orderline = Orderline(order_id="789", sku="MEMORY", quantity=1)
    ref = allocate(orderline, [batch_1, batch_2])
    assert ref == batch_1.id


def test_batch_equality():
    batch_1 = Batch(id="1", sku="THIS", purchased_quantity=1)
    batch_2 = Batch(id="1", sku="THAT", purchased_quantity=2)
    assert batch_1 == batch_2


def test_batch_inequality():
    batch_1 = Batch(id="1", sku="THIS", purchased_quantity=1)
    batch_2 = Batch(id="2", sku="THIS", purchased_quantity=2)
    assert batch_1 != batch_2


def test_batch_line_inequality():
    batch = Batch(id="1", sku="THIS", purchased_quantity=1)
    line = Orderline(order_id="1", sku="THAT", quantity=1)
    assert batch != line
