import json

import pandas as pd
import streamlit as st

from ai_engine import get_recommendations
from feature_builder import normalize_columns, coerce_numeric, add_metrics, build_features
from json_parser import parse_ai_json
from simulation_ai_based import simulate_ai_spend

st.set_page_config(page_title="AI Amazon Ads Optimizer", layout="wide")

st.title("AI Amazon Ads Optimization")

provider = st.selectbox("AI Model", ["claude", "openai"], index=1)

book_title = st.text_input("Book Title")
# book_description = st.text_area("Book Description")

files_up = st.file_uploader("Upload Amazon Ads CSVs", type="csv", accept_multiple_files=True)

if files_up and book_title:
    frames = []
    for f in files_up:
        df = pd.read_csv(f)
        df = normalize_columns(df)
        df = coerce_numeric(df)
        df = add_metrics(df)
        df["Source"] = f.name
        frames.append(df)

    full = pd.concat(frames, ignore_index=True)

    st.write("Dataset Loaded:", full.shape)

    features = build_features(full)

    user_prompt = f"""
    You will receive:
    1. Book title
    2. Book description
    3. Amazon Ads metric dataset

    Your job:
    Produce:
    A. Global book performance analysis
    B. Target-level recommendations using Amazon bidding logic
    C. Keyword relevance scoring to the book
    D. Dataset efficiency summary
    E. Spend interpretation commentary

    BOOK:
    Title: {book_title}
    Description: <search web for 'About {book_title} Book'>

    DATA:
    {json.dumps(features, indent=2)}

    Your response MUST be structured EXACTLY as:

    {{
      "global_summary": {{
        "book_title": "{book_title}",
        "overall_ads_health": "<interpret ACOS, ROAS, CTR, spend, conversion>",
        "total_spend_usd": string,
        "efficiency_commentary": "<high/low spend interpretation>",
        "keyword_volume_strength": "<opportunity direction>",
        "primary_recommendation_direction": "<scale vs reduce>"
      }},

      "keyword_relevance_analysis": [
        {{
          "target": "string",
          "relevance_score": 0-100,
          "relevance_reason": "why keyword matches or doesn’t match book topic"
        }}
      ],

      "recommendations_per_target": [
        {{
          "target": "string",
          "current_acos": number or null,
          "current_roas": number or null,
          "orders": number,
          "spend_usd": number,
          "sales_usd": number,
          "ctr": number or null,
          "relevance_score": 0-100,
          "decision": "increase_bid | decrease_bid | pause | negative_target | hold | scale",
          "bid_adjustment_pct": number,
          "confidence": "low | medium | high",
          "justification": "must cite numeric evidence"
        }}
      ]
    }}
    """

    if st.button("Run AI Optimization"):
        with st.spinner("AI reading dataset..."):
            raw = get_recommendations(provider, user_prompt)
            print(raw)
            parsed = parse_ai_json(raw)

        summary = parsed["global_summary"]
        relevance = parsed["keyword_relevance_analysis"]
        rec_data = parsed["recommendations_per_target"]

        st.subheader(f"Book Title : {summary['book_title']}")

        st.divider()

        st.subheader("Overall Ads Health")
        st.caption(summary['overall_ads_health'])

        st.divider()

        st.subheader("Efficiency Commentary")
        st.caption(summary['efficiency_commentary'])

        st.divider()

        st.subheader("Keyword Volume Strength ")
        st.caption(summary['keyword_volume_strength'])

        st.divider()

        st.subheader("Primary Recommendation")
        st.badge(summary['primary_recommendation_direction'])

        st.divider()

        st.header('Keyword relevance analysis')
        st.dataframe(pd.DataFrame(relevance))

        st.header('Recommendations per target')
        st.dataframe(pd.DataFrame(rec_data))

        sim = simulate_ai_spend(rec_data)
        st.subheader("Simulated Spend Impact from AI Decisions")

        st.divider()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Before Spend", sim['before_spend'])
        c2.metric("After Spend", sim['after_spend'])
        c3.metric("Savings (USD)", sim['savings_usd'])
        c4.metric("Savings %", sim['savings_pct'])
