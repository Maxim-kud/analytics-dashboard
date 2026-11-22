import os
from datetime import date, timedelta

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import CheckConstraint, Date, Float, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

load_dotenv()


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("amount > 0", name="amount_positive"),
        CheckConstraint("kind IN ('Доход', 'Расход')", name="kind_allowed"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    note: Mapped[str] = mapped_column(String(200), default="")


def get_engine():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL не задан. Скопируйте .env.example в .env.")
    return create_engine(url, pool_pre_ping=True)


def initialize(engine):
    Base.metadata.create_all(engine)


def add_transaction(engine, day, kind, category, amount, note=""):
    if amount <= 0 or kind not in ("Доход", "Расход"):
        raise ValueError("Некорректная операция")
    with Session(engine) as session:
        session.add(Transaction(date=day, kind=kind, category=category, amount=float(amount), note=note))
        session.commit()


def delete_transaction(engine, transaction_id):
    with Session(engine) as session:
        item = session.get(Transaction, int(transaction_id))
        if item:
            session.delete(item)
            session.commit()


def fetch_transactions(engine):
    with Session(engine) as session:
        rows = session.scalars(select(Transaction).order_by(Transaction.date.desc(), Transaction.id.desc())).all()
        return pd.DataFrame(
            [{"id": x.id, "date": x.date, "kind": x.kind, "category": x.category,
              "amount": x.amount, "note": x.note} for x in rows],
            columns=["id", "date", "kind", "category", "amount", "note"],
        )


def seed_demo(engine):
    with Session(engine) as session:
        if session.scalar(select(Transaction.id).limit(1)) is not None:
            return False
        today = date.today().replace(day=1)
        samples = [
            (0, "Доход", "Зарплата", 95000, "Основной доход"),
            (0, "Расход", "Продукты", 18500, "Покупки"),
            (0, "Расход", "Транспорт", 5200, "Проезд"),
            (0, "Расход", "Развлечения", 6800, "Кино и кафе"),
            (1, "Доход", "Зарплата", 92000, "Основной доход"),
            (1, "Расход", "Продукты", 16700, "Покупки"),
            (2, "Доход", "Подработка", 24000, "Проект"),
            (2, "Расход", "Транспорт", 4300, "Проезд"),
        ]
        for months_ago, kind, category, amount, note in samples:
            month = today.month - months_ago
            year = today.year
            while month <= 0:
                month += 12
                year -= 1
            session.add(Transaction(date=date(year, month, 5), kind=kind,
                                    category=category, amount=amount, note=note))
        session.commit()
        return True
