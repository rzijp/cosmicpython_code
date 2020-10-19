from datetime import date, timedelta

import pytest

from model import Batch, Orderline

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_can_allocate_if_available_greater_than_required():
    batch = Batch(id="123", sku="RED CHAIR", quantity=10)
    orderline = Orderline(sku="RED CHAIR", quantity=2)
    assert batch.allocate(orderline)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch(id="123", sku="RED CHAIR", quantity=10)
    orderline = Orderline(sku="RED CHAIR", quantity=2)
    batch.allocate(orderline)
    assert batch.quantity == 8


def test_cannot_allocate_if_available_smaller_than_required():
    batch = Batch(id="123", sku="RED CHAIR", quantity=10)
    orderline = Orderline(sku="RED CHAIR", quantity=20)
    assert not (batch.allocate(orderline))


def test_can_allocate_if_available_equal_to_required():
    batch = Batch(id="123", sku="RED CHAIR", quantity=10)
    orderline = Orderline(sku="RED CHAIR", quantity=10)
    batch.allocate(orderline)
    assert batch.quantity == 0


@pytest.mark.xfail()
def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


@pytest.mark.xfail()
def test_prefers_earlier_batches():
    pytest.fail("todo")
