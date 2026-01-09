import streamlit as st
import requests
import json

# -----------------------------
# API CONFIG
# -----------------------------
RUN_API_URL = "http://127.0.0.1:8000/run"
INGEST_API_URL = "http://127.0.0.1:8000/ingest-and-analyze"

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Marketing Intelligence",
    layout="wide",
)

st.title("🧠 AI Marketing Intelligence")
st.caption(
    "Behavioral segmentation and campaign recommendations powered by Agentic AI"
)

# -----------------------------
# DOMAIN SELECTOR
# -----------------------------
domain = st.selectbox(
    "Select Business Domain",
    ["supermarket", "oil", "banking"],
)

# =========================================================
# LIVE DATA INGESTION
# =========================================================
st.subheader("📥 Optional: Live Data Ingestion")

col1, col2, col3 = st.columns(3)

with col1:
    customers_file = st.file_uploader(
        "Upload customers.json",
        type=["json"],
        key="customers",
    )

with col2:
    transactions_file = st.file_uploader(
        "Upload transactions.json",
        type=["json"],
        key="transactions",
    )

with col3:
    campaigns_file = st.file_uploader(
        "Upload past_campaigns.json",
        type=["json"],
        key="campaigns",
    )

use_uploaded_data = (
    customers_file is not None
    and transactions_file is not None
    and campaigns_file is not None
)

if use_uploaded_data:
    st.success("Live data loaded. Analysis will use uploaded data.")
else:
    st.info("No data uploaded. Default dataset will be used.")

# -----------------------------
# RUN BUTTON
# -----------------------------
run_button = st.button("🚀 Run AI Analysis")

# =========================================================
# API CALL
# =========================================================
if run_button:
    with st.spinner("Running AI pipeline..."):
        try:
            # ----------------------------------
            # CASE 1: Live ingestion
            # ----------------------------------
            if use_uploaded_data:
                customers = json.load(customers_file)
                transactions = json.load(transactions_file)
                past_campaigns = json.load(campaigns_file)

                payload = {
                    "domain": domain,
                    "customers": customers,
                    "transactions": transactions,
                    "past_campaigns": past_campaigns,
                }

                response = requests.post(
                    INGEST_API_URL,
                    json=payload,
                    timeout=120,
                )

                results = response.json()

            # ----------------------------------
            # CASE 2: Default pipeline
            # ----------------------------------
            else:
                response = requests.post(
                    RUN_API_URL,
                    json={"domain": domain},
                    timeout=120,
                )

                if response.status_code != 200:
                    st.error(response.text)
                    st.stop()

                results = response.json()["results"]

            # ----------------------------------
            # RENDER RESULTS
            # ----------------------------------
            st.success(f"Analysis completed for **{domain.upper()}**")

            for r in results:
                with st.expander(
                    f"👤 Customer {r['customer_id']} | Segment: {r['segment']}",
                    expanded=False,
                ):
                    col1, col2 = st.columns(2)

                    # -----------------------------
                    # LEFT: SIGNALS
                    # -----------------------------
                    with col1:
                        st.subheader("📊 Behavioral Signals")

                        if r["signals"]:
                            st.json(r["signals"])
                        else:
                            st.info("No behavioral signals available")

                    # -----------------------------
                    # RIGHT: CAMPAIGN
                    # -----------------------------
                    with col2:
                        st.subheader("🎯 Recommended Campaign")

                        campaign = r["campaign"]

                        st.markdown(
                            f"""
                            **Type:** {campaign['campaign_type']}  
                            **Channel:** {campaign['channel']}  
                            **Duration:** {campaign['duration_days']} days  
                            **Estimated Participation:** {campaign['estimated_participation_rate'] * 100:.0f}%  
                            **Estimated Cost:** ₹{campaign['estimated_cost']:,}  
                            **Estimated Revenue:** ₹{campaign['estimated_revenue']:,}  
                            **Estimated ROI:** {campaign['estimated_roi']}x  
                            """
                        )

                        st.markdown(
                            f"**Message Preview:**\n\n> {campaign['message']}"
                        )

                    # -----------------------------
                    # REASONING
                    # -----------------------------
                    st.subheader("🧠 AI Reasoning")

                    reasoning = r["reasoning"]
                    st.markdown(reasoning["llm_explanation"])

                    st.caption(
                        f"Confidence: {reasoning['confidence']} | "
                        f"Business Risk: {reasoning['business_risk']}"
                    )

        except Exception as e:
            st.error(f"API error: {str(e)}")
