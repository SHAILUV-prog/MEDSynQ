import streamlit as st

# data from rd
p2_data = {
    "spo2_trend": "declining",
    "heart_rate_trend": "increasing",
    "deterioration": True,
    "risk": "HIGH",
    "score": 7
}
# data from sri
p3_data = {
    "evidence": [
        {
            "source": "NEWS2 Guidance",
            "relevance": 0.92
        },
        {
            "source": "Respiratory Guidance",
            "relevance": 0.88
        }
    ]
}

st.title("CareSync AI")

st.header("P2 - Trend & Safety")

st.write("SpO₂ Trend:", p2_data["spo2_trend"])
st.write("Heart Rate Trend:", p2_data["heart_rate_trend"])
st.write("Deterioration:", p2_data["deterioration"])
st.write("Risk:", p2_data["risk"])
st.write("Safety Score:", p2_data["score"])

st.header("P3 - Medical Evidence")

for item in p3_data["evidence"]:
    st.write(item["source"], "| Relevance:", item["relevance"])