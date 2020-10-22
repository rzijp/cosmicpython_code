from allocation.domain import model
from allocation.adapters.repository import SqlAlchemyRepository


def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "TEST_SKU", 100, eta=None)

    repo = SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = list(
        session.execute(
            'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
        )
    )
    assert rows == [("batch1", "TEST_SKU", 100, None)]
