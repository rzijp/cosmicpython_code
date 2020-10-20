from datetime import date, timedelta
from typing import Tuple

import pytest

from model import Batch, Orderline

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def create_batch_and_orderline(
    sku: str, batch_quantity: int, orderline_quantity: int
) -> Tuple[Batch, Orderline]:
    batch = Batch(id="123", sku=sku, available_quantity=batch_quantity)
    orderline = Orderline(sku=sku, quantity=orderline_quantity)
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
    batch = Batch("123", sku="GREEN TABLE", available_quantity=10)
    wrong_sku_orderline = Orderline(sku="RED CHAIR", quantity=2)
    assert batch.can_allocate(wrong_sku_orderline) is False


@pytest.mark.xfail()
def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


@pytest.mark.xfail()
def test_prefers_earlier_batches():
    pytest.fail("todo")
