from allocation.domain import model


def test_orderline_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        "('order1', 'RED-CHAIR', 12),"
        "('order1', 'RED-TABLE', 13),"
        "('order2', 'BLUE-LIPSTICK', 14)"
    )
    expected = [
        model.Orderline("order1", "RED-CHAIR", 12),
        model.Orderline("order1", "RED-TABLE", 13),
        model.Orderline("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(model.Orderline).all() == expected