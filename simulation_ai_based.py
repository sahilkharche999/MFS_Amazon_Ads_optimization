import pandas as pd


def simulate_ai_spend(rec_data):
    df = pd.DataFrame(rec_data)

    if not {"decision", "bid_adjustment_pct", "spend_usd"} <= set(df.columns):
        return {
            "error": True,
            "message": "missing required fields"
        }

    df["new_spend"] = df.apply(_compute_new_spend, axis=1)

    before = df["spend_usd"].sum()
    after = df["new_spend"].sum()

    return {
        "before_spend": round(before, 2),
        "after_spend": round(after, 2),
        "savings_usd": round(before - after, 2),
        "savings_pct": round(((before - after) / before) * 100, 2) if before > 0 else None
    }


def _compute_new_spend(row):
    dec = row["decision"]
    pct = (row.get("bid_adjustment_pct") or 0) / 100
    old = row["spend_usd"]

    if dec == "increase_bid":
        return old * (1 + pct)

    if dec == "decrease_bid":
        return old * (1 - pct)

    if dec in ["pause", "negative_target"]:
        return 0.0

    return old
