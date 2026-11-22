from datetime import date

import plotly.express as px
import streamlit as st

from services.database import (
    add_transaction, delete_transaction, fetch_transactions, get_engine, initialize, seed_demo
)
from utils.analytics import category_expenses, monthly_totals, summarize

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 1.6rem; max-width: 1280px;}
h1 {letter-spacing: -.03em;}
[data-testid="stMetric"] {background: #17263d; padding: 16px; border-radius: 14px;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Analytics Dashboard")
st.caption("Финансовая аналитика • PostgreSQL + Streamlit + Plotly")

try:
    engine = get_engine()
    initialize(engine)
    df = fetch_transactions(engine)
except Exception as exc:
    st.error(f"Не удалось подключиться к PostgreSQL: {exc}")
    st.info("Запустите `docker compose up -d --wait` и проверьте файл .env.")
    st.stop()

with st.sidebar:
    st.header("Новая операция")
    with st.form("new_transaction", clear_on_submit=True):
        day = st.date_input("Дата", date.today())
        kind = st.selectbox("Тип", ["Расход", "Доход"])
        category = st.selectbox("Категория", [
            "Продукты", "Транспорт", "Развлечения", "Жильё", "Зарплата", "Подработка", "Другое"
        ])
        amount = st.number_input("Сумма, ₽", min_value=0.01, value=1000.0, step=100.0)
        note = st.text_input("Комментарий", max_chars=200)
        submitted = st.form_submit_button("Добавить", use_container_width=True)
    if submitted:
        add_transaction(engine, day, kind, category, amount, note)
        st.rerun()
    st.divider()
    if st.button("Заполнить демо-данными", use_container_width=True):
        if seed_demo(engine):
            st.rerun()
        else:
            st.info("Таблица уже содержит операции.")

st.subheader("Фильтры")
f1, f2, f3 = st.columns([1, 1, 2])
with f1:
    start = st.date_input("С", value=date.today().replace(month=1, day=1), key="start")
with f2:
    end = st.date_input("По", value=date.today(), key="end")
with f3:
    options = sorted(df["category"].unique().tolist())
    selected = st.multiselect("Категории", options, default=options)

if start > end:
    st.warning("Начальная дата позже конечной.")
    st.stop()

filtered = df.loc[
    (df["date"] >= start) & (df["date"] <= end) & (df["category"].isin(selected))
].copy()
stats = summarize(filtered)
m1, m2, m3 = st.columns(3)
m1.metric("Доходы", f"{stats['income']:,.0f} ₽")
m2.metric("Расходы", f"{stats['expense']:,.0f} ₽")
m3.metric("Баланс", f"{stats['balance']:,.0f} ₽")

left, right = st.columns([1.6, 1])
with left:
    st.subheader("Динамика по месяцам")
    monthly = monthly_totals(filtered)
    if monthly.empty:
        st.info("Нет данных за выбранный период.")
    else:
        fig = px.bar(monthly, x="month", y="amount", color="kind", barmode="group",
                     labels={"month": "Месяц", "amount": "Сумма, ₽", "kind": "Тип"},
                     color_discrete_map={"Доход": "#35c4a2", "Расход": "#ff7a91"})
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Структура расходов")
    expenses = category_expenses(filtered)
    if expenses.empty:
        st.info("Расходов пока нет.")
    else:
        fig = px.pie(expenses, names="category", values="amount", hole=.58)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Операции")
if filtered.empty:
    st.info("Операций пока нет. Добавьте первую или загрузите демо-данные.")
else:
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    with st.expander("Удалить операцию"):
        ids = filtered["id"].astype(int).tolist()
        item_id = st.selectbox("ID операции", ids)
        if st.button("Удалить выбранную операцию", type="secondary"):
            delete_transaction(engine, item_id)
            st.rerun()
