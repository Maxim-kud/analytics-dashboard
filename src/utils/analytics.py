import pandas as pd


def summarize(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"income": 0.0, "expense": 0.0, "balance": 0.0}
    income = float(df.loc[df["kind"] == "Доход", "amount"].sum())
    expense = float(df.loc[df["kind"] == "Расход", "amount"].sum())
    return {"income": income, "expense": expense, "balance": income - expense}


def monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["month", "kind", "amount"])
    data = df.copy()
    data["month"] = pd.to_datetime(data["date"]).dt.to_period("M").astype(str)
    return data.groupby(["month", "kind"], as_index=False)["amount"].sum()


def category_expenses(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])
    return df.loc[df["kind"] == "Расход"].groupby("category", as_index=False)["amount"].sum()
