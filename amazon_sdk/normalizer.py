
def normalize_keyword_row(row):
    cost = row.get("cost", 0)
    sales = row.get("attributedSales14d", 0)

    acos = round((cost / sales) * 100, 2) if sales else None

    return {
        "campaignId": row.get("campaignId"),
        "adGroupId": row.get("adGroupId"),
        "keyword": row.get("keywordText"),
        "matchType": row.get("matchType"),
        "impressions": row.get("impressions"),
        "clicks": row.get("clicks"),
        "spend": cost,
        "sales": sales,
        "acos": acos,
    }
