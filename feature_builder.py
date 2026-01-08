# ======================================================
# DEFINITIVE COLUMN MAP BASED ON YOUR CSV STRUCTURE
# ======================================================
COLUMN_MAP = {
    "state": "State",
    "categories & products": "Target",
    "status": "Status",

    "suggested bid (low)(usd)": "Suggested bid (low)",
    "suggested bid (median)(usd)": "Suggested bid (median)",
    "suggested bid (high)(usd)": "Suggested bid (high)",
    "target bid(usd)": "Target bid",

    "top-of-search is": "Top of search IS",

    "impressions": "Impressions",
    "clicks": "Clicks",
    "ctr": "CTR",
    "cpc(usd)": "CPC",
    "spend(usd)": "Spend",
    "sales(usd)": "Sales",

    "orders": "Orders",
    "acos": "ACOS",

    "kenp read": "KENP read",
    "estimated kenp royalties(usd)": "KENP royalties"
}


# ======================================================
# COLUMN NORMALIZATION
# ======================================================
def normalize_columns(df):
    rename = {}
    for c in df.columns:
        key = c.strip().lower()
        if key in COLUMN_MAP:
            rename[c] = COLUMN_MAP[key]
    return df.rename(columns=rename)


# ======================================================
# NUMERIC CLEANING
# ======================================================
def coerce_numeric(df):
    numeric_fields = [
        "Impressions", "Clicks", "Orders",
        "Spend", "Sales", "CPC",
        "CTR", "ACOS",
        "KENP read", "KENP royalties",
        "Target bid",
        "Suggested bid (low)", "Suggested bid (median)", "Suggested bid (high)"
    ]

    for col in numeric_fields:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[$,%]", "", regex=True)
                .replace("-", "0")
                .astype(float)
                .fillna(0.0)
            )

    return df


# ======================================================
# DERIVED VALUES
# ======================================================
def add_metrics(df):
    # CTR if missing
    if "CTR" not in df.columns and {"Clicks", "Impressions"} <= set(df.columns):
        df["CTR"] = df.apply(
            lambda r: r["Clicks"] / r["Impressions"] if r["Impressions"] > 0 else None,
            axis=1
        )

    # ACoS if missing
    if "ACOS" not in df.columns and {"Spend", "Sales"} <= set(df.columns):
        df["ACOS"] = df.apply(
            lambda r: r["Spend"] / r["Sales"] if r["Sales"] > 0 else None,
            axis=1
        )

    # ROAS always derived
    if {"Spend", "Sales"} <= set(df.columns):
        df["ROAS (Derived)"] = df.apply(
            lambda r: r["Sales"] / r["Spend"] if r["Spend"] > 0 else None,
            axis=1
        )

    return df


# ======================================================
# MASTER FEATURE BUILDER OUTPUT FOR AI ENGINE
# ======================================================
def build_features(df):
    feats = []

    for _, r in df.iterrows():
        feats.append({

            "state": r.get("State"),
            "status": r.get("Status"),

            # Book Target Data
            "target": r.get("Target"),

            # Spend & Performance
            "impressions": int(r.get("Impressions", 0)),
            "clicks": int(r.get("Clicks", 0)),
            "orders": int(r.get("Orders", 0)),
            "spend_usd": round(r.get("Spend", 0.0), 2),
            "sales_usd": round(r.get("Sales", 0.0), 2),

            # Amazon Core Metrics
            "ctr": r.get("CTR"),
            "cpc": r.get("CPC"),
            "acos": r.get("ACOS"),
            "roas_derived": r.get("ROAS (Derived)"),

            # Keyword Bid Data
            "current_bid": r.get("Target bid"),
            "suggested_low": r.get("Suggested bid (low)"),
            "suggested_median": r.get("Suggested bid (median)"),
            "suggested_high": r.get("Suggested bid (high)"),

            # Ranking Signal
            "top_of_search": r.get("Top of search IS"),

            # Kindle performance
            "kenp_read": r.get("KENP read"),
            "kenp_royalties": r.get("KENP royalties")

        })

    return feats
