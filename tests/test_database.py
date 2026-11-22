from datetime import date
import pytest
from src.services.database import add_transaction


def test_rejects_invalid_amount_without_db_connection():
    with pytest.raises(ValueError):
        add_transaction(None, date(2026, 1, 1), "Доход", "Зарплата", 0)


def test_rejects_invalid_kind_without_db_connection():
    with pytest.raises(ValueError):
        add_transaction(None, date(2026, 1, 1), "Неизвестно", "Другое", 10)
