from datetime import date
import pandas as pd
from src.utils.analytics import summarize, monthly_totals, category_expenses


def sample():
    return pd.DataFrame([
        {"date": date(2026, 1, 1), "kind": "Доход", "category": "Зарплата", "amount": 100.0},
        {"date": date(2026, 1, 2), "kind": "Расход", "category": "Продукты", "amount": 30.0},
        {"date": date(2026, 2, 2), "kind": "Расход", "category": "Продукты", "amount": 20.0},
    ])


def test_summary():
    assert summarize(sample()) == {"income": 100.0, "expense": 50.0, "balance": 50.0}


def test_empty():
    assert summarize(pd.DataFrame())["balance"] == 0.0


def test_monthly():
    assert monthly_totals(sample())["amount"].sum() == 150.0


def test_categories():
    assert category_expenses(sample()).iloc[0]["amount"] == 50.0
