import streamlit as st
from pypdf import PdfReader


# =========================================================
# 1. PDF TEXT EXTRACTION
# =========================================================

def extract_pdf_text(uploaded_file):
    """Extract text from an uploaded PDF."""

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# =========================================================
# 2. GET PATIENT INPUT
# =========================================================

def get_patient_input():
    """Get patient information from text or PDF."""

    st.subheader("👤 Patient Information")

    input_method = st.radio(
        "How do you want to provide patient details?",
        ["Enter Text", "Upload PDF"]
    )

    patient_text = ""

    # -----------------------------------------------------
    # TEXT INPUT
    # -----------------------------------------------------

    if input_method == "Enter Text":

        patient_text = st.text_area(
            "Enter patient details",
            height=220,
            placeholder="""
Example:

Patient ID: P001
Age: 62
Sex: Male
Symptoms: Fever, cough, shortness of breath
Medical History: Diabetes, hypertension
Medication: Metformin
SpO2: 91%
Heart Rate: 108
Temperature: 38.5 C
"""
        )

    # -----------------------------------------------------
    # PDF INPUT
    # -----------------------------------------------------

    else:

        uploaded_file = st.file_uploader(
            "Upload patient report",
            type=["pdf"]
        )

        if uploaded_file is not None:

            patient_text = extract_pdf_text(uploaded_file)

            st.success("✅ PDF uploaded successfully!")

            with st.expander("📄 View extracted patient information"):

                st.text(patient_text)

    return patient_text


# =========================================================
# 3. MOCK P1 PIPELINE
# =========================================================

def run_p1(patient_text):
    """
    TEMPORARY MOCK P1.

    Later this will be replaced with the real P1 pipeline:
    
    Intake Agent
        ↓
    Structured JSON
        ↓
    Clinical Agent
        ↓
    Clinical analysis
    """

    p1_result = {

        "patient_text": patient_text,

        "clinical_summary":
            "Clinical information extracted and analyzed successfully.",

        "possible_conditions": [
            "Respiratory infection",
            "Fever-related illness"
        ],

        "potential_risks": [
            "Respiratory deterioration"
        ]
    }

    return p1_result


# =========================================================
# 4. MOCK P2 PIPELINE
# =========================================================

def run_p2(p1_result):
    """
    TEMPORARY MOCK P2.

    Later this will be replaced with:

    Trend Engine
        +
    Safety Engine
        +
    Patient Database
    """

    p2_result = {

        "risk": "HIGH",

        "score": 7,

        "spo2_trend": "Declining",

        "heart_rate_trend": "Increasing",

        "deterioration": True,

        "safety_alerts": [
            "Low oxygen saturation",
            "Elevated heart rate"
        ]
    }

    return p2_result


# =========================================================
# 5. MOCK P3 PIPELINE
# =========================================================

def run_p3(p1_result, p2_result):
    """
    TEMPORARY MOCK P3.

    Later this will be replaced with
    the real RAG / evidence engine.
    """

    p3_result = {

        "evidence": [
            "NEWS2 clinical guidance",
            "Respiratory clinical guidance"
        ],

        "evidence_relevance": [
            "92%",
            "88%"
        ]
    }

    return p3_result


# =========================================================
# 6. MOCK CARE COORDINATOR
# =========================================================

def run_care_coordinator(
    p1_result,
    p2_result,
    p3_result
):
    """
    TEMPORARY MOCK CARE COORDINATOR.

    Later P1's real Care Coordinator
    will perform this synthesis.
    """

    risk = p2_result["risk"]

    if risk == "HIGH":

        recommendation = (
            "Immediate clinical assessment is recommended."
        )

        summary = (
            "The available patient information indicates "
            "potential clinical deterioration."
        )

    elif risk == "MODERATE":

        recommendation = (
            "Further clinical evaluation and monitoring "
            "are recommended."
        )

        summary = (
            "The patient shows some findings that may "
            "require additional clinical monitoring."
        )

    else:

        recommendation = (
            "Continue routine monitoring and follow-up."
        )

        summary = (
            "No major deterioration indicators were "
            "identified in the available information."
        )

    final_result = {

        "risk_level": risk,

        "risk_score": p2_result["score"],

        "summary": summary,

        "recommended_action": recommendation,

        "clinical_analysis":
            p1_result["clinical_summary"],

        "possible_conditions":
            p1_result["possible_conditions"],

        "potential_risks":
            p1_result["potential_risks"],

        "spo2_trend":
            p2_result["spo2_trend"],

        "heart_rate_trend":
            p2_result["heart_rate_trend"],

        "deterioration":
            p2_result["deterioration"],

        "safety_alerts":
            p2_result["safety_alerts"],

        "evidence":
            p3_result["evidence"],

        "requires_human_review": True
    }

    return final_result


# =========================================================
# 7. STREAMLIT PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CareSync AI",
    page_icon="🏥",
    layout="wide"
)


# =========================================================
# 8. HEADER
# =========================================================

st.title("🏥 CareSync AI")

st.write(
    "Clinical Decision Support Prototype"
)

st.divider()


# =========================================================
# 9. PATIENT INPUT
# =========================================================

patient_text = get_patient_input()


# =========================================================
# 10. ANALYZE BUTTON
# =========================================================

if st.button(
    "🔍 Analyze Patient",
    type="primary",
    use_container_width=True
):

    if not patient_text.strip():

        st.warning(
            "⚠️ Please enter or upload patient information."
        )

    else:

        # =================================================
        # P1
        # =================================================

        with st.spinner(
            "🤖 Running Clinical Analysis..."
        ):

            p1_result = run_p1(
                patient_text
            )


        # =================================================
        # P2
        # =================================================

        with st.spinner(
            "🛡️ Analyzing Trends & Safety..."
        ):

            p2_result = run_p2(
                p1_result
            )


        # =================================================
        # P3
        # =================================================

        with st.spinner(
            "📚 Retrieving Clinical Evidence..."
        ):

            p3_result = run_p3(
                p1_result,
                p2_result
            )


        # =================================================
        # CARE COORDINATOR
        # =================================================

        with st.spinner(
            "🧠 Synthesizing Final Assessment..."
        ):

            final_result = run_care_coordinator(
                p1_result,
                p2_result,
                p3_result
            )


        # =================================================
        # RESULTS
        # =================================================

        st.divider()

        st.header("📊 Patient Analysis")


        # =================================================
        # CLINICAL ANALYSIS
        # =================================================

        st.subheader("🤖 Clinical Analysis")

        st.write(
            final_result["clinical_analysis"]
        )


        # Possible conditions

        if final_result["possible_conditions"]:

            st.write("**Possible Conditions:**")

            for condition in final_result[
                "possible_conditions"
            ]:

                st.write(
                    "•",
                    condition
                )


        # Potential risks

        if final_result["potential_risks"]:

            st.write("**Potential Risks:**")

            for risk in final_result[
                "potential_risks"
            ]:

                st.write(
                    "•",
                    risk
                )


        # =================================================
        # RISK & SAFETY
        # =================================================

        st.subheader("🛡️ Risk & Safety")

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Risk Level",
                final_result["risk_level"]
            )


        with col2:

            st.metric(
                "Risk Score",
                f"{final_result['risk_score']}/10"
            )


        with col3:

            st.metric(
                "Deterioration",
                "YES"
                if final_result["deterioration"]
                else "NO"
            )


        # Trends

        st.write(
            f"**SpO₂ Trend:** "
            f"{final_result['spo2_trend']}"
        )

        st.write(
            f"**Heart Rate Trend:** "
            f"{final_result['heart_rate_trend']}"
        )


        # Safety alerts

        if final_result["safety_alerts"]:

            st.write("**Safety Alerts:**")

            for alert in final_result[
                "safety_alerts"
            ]:

                st.warning(
                    f"⚠️ {alert}"
                )


        # =================================================
        # SUPPORTING EVIDENCE
        # =================================================

        st.subheader("📚 Supporting Evidence")

        for evidence in final_result[
            "evidence"
        ]:

            st.write(
                "•",
                evidence
            )


        # =================================================
        # FINAL RESULT
        # =================================================

        st.divider()

        st.header("🎯 Final Result")


        # Risk display

        if final_result["risk_level"] == "HIGH":

            st.error(
                "🔴 HIGH RISK"
            )

        elif final_result["risk_level"] == "MODERATE":

            st.warning(
                "🟠 MODERATE RISK"
            )

        else:

            st.success(
                "🟢 LOW RISK"
            )


        # Risk score

        st.metric(
            "Patient Risk Score",
            f"{final_result['risk_score']}/10"
        )


        # Summary

        st.subheader("📝 Clinical Summary")

        st.write(
            final_result["summary"]
        )


        # =================================================
        # RECOMMENDED ACTION
        # =================================================

        st.subheader("📋 Recommended Action")

        st.info(
            final_result["recommended_action"]
        )


        # =================================================
        # HUMAN REVIEW
        # =================================================

        st.divider()

        st.header("👨‍⚕️ Human Review")

        st.write(
            "Review the AI-generated assessment "
            "and recommendation before taking action."
        )


        # Review box

        st.subheader(
            "AI Recommendation"
        )

        st.write(
            final_result[
                "recommended_action"
            ]
        )

        st.write(
            f"**Risk Level:** "
            f"{final_result['risk_level']}"
        )

        st.write(
            f"**Risk Score:** "
            f"{final_result['risk_score']}/10"
        )


        # =================================================
        # APPROVE / REJECT
        # =================================================

        col1, col2 = st.columns(2)


        with col1:

            approve = st.button(
                "✅ Approve Recommendation",
                use_container_width=True
            )


        with col2:

            reject = st.button(
                "❌ Reject Recommendation",
                use_container_width=True
            )


        # =================================================
        # REVIEW STATUS
        # =================================================

        if approve:

            st.session_state[
                "review_status"
            ] = "APPROVED"


        if reject:

            st.session_state[
                "review_status"
            ] = "REJECTED"


        if "review_status" in st.session_state:

            if st.session_state[
                "review_status"
            ] == "APPROVED":

                st.success(
                    "✅ Recommendation approved "
                    "by human reviewer."
                )

            else:

                st.warning(
                    "❌ Recommendation rejected "
                    "by human reviewer."
                )