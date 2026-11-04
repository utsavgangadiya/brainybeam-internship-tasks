
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import joblib
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------



BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "saved_models" / "heart_disease_model_v1.joblib"

model = joblib.load(MODEL_PATH)

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"Unable to load model: {e}")
    st.stop()

FEATURES = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak"
]

if not hasattr(model, "n_features_in_") or model.n_features_in_ != len(FEATURES):
    st.error("The model does not match the five expected input features.")
    st.stop()

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: #F4F7FB;
    color: #172B4D;
    font-family: 'Segoe UI', sans-serif;
}

/* Main content */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */
.main-title {
    font-size: 36px;
    font-weight: 750;
    color: #123B63;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 15px;
    color: #52677F;
    margin-bottom: 25px;
}

/* Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #DCE5EF;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 3px 12px rgba(20, 50, 80, 0.05);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 7px 20px rgba(20, 50, 80, 0.10);
}

/* Buttons */
.stButton > button {
    background: #176B87;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 22px;
    font-weight: 600;
    transition: background 0.2s ease, transform 0.2s ease;
}

.stButton > button:hover {
    background: #10536B;
    color: white;
    transform: translateY(-2px);
}

/* Inputs */
.stNumberInput input {
    background: #FFFFFF;
    border-radius: 8px;
    border-color: #C8D5E3;
}

.stNumberInput label {
    color: #243F5C;
    font-weight: 600;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #DCE5EF;
    border-radius: 12px;
    padding: 16px;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Smooth entrance */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.main .block-container {
    animation: fadeIn 0.5s ease-out;
}

/* Accessibility focus */
.stButton button:focus-visible,
input:focus-visible {
    outline: 3px solid #F0A830 !important;
    outline-offset: 3px;
}

/* Responsive design */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .main-title {
        font-size: 26px;
    }

    .subtitle {
        font-size: 13px;
    }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="main-title">
    ❤️ Heart Disease Prediction
</div>

<div class="subtitle">
    Machine Learning Based Health Risk Analysis Dashboard
</div>
""", unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# PATIENT INPUT SECTION
# --------------------------------------------------

st.subheader("Patient Information")

st.write(
    "Enter the following measurements to generate a model prediction."
)

with st.container(border=True):

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age (years)",
            min_value=1,
            max_value=120,
            value=45,
            step=1
        )

        trestbps = st.number_input(
            "Resting Blood Pressure",
            min_value=50,
            max_value=250,
            value=120,
            step=1
        )

        chol = st.number_input(
            "Serum Cholesterol",
            min_value=50,
            max_value=700,
            value=200,
            step=1
        )

    with col2:
        thalach = st.number_input(
            "Maximum Heart Rate",
            min_value=40,
            max_value=250,
            value=150,
            step=1
        )

        oldpeak = st.number_input(
            "Oldpeak",
            min_value=0.0,
            max_value=10.0,
            value=1.2,
            step=0.1
        )

st.write(
    "This model uses the five features "
    "used when training the model."
)

# --------------------------------------------------
# PREDICTION BUTTON
# --------------------------------------------------

st.write("")

predict_button = st.button(
    "Generate Prediction",
    use_container_width=True
)

# --------------------------------------------------
# PREDICTION FUNCTIONALITY
# --------------------------------------------------

if predict_button:

    input_data = pd.DataFrame(
        [[age, trestbps, chol, thalach, oldpeak]],
        columns=FEATURES
    )

    try:
        with st.spinner("Analyzing input values..."):

            prediction = model.predict(input_data)[0]

            probabilities = None

            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(input_data)[0]

        st.divider()

        st.subheader("Prediction Results")

        if prediction == 1:
            st.error(
                "Model Prediction: Positive"
            )
            st.write(
                "The model predicts the positive class."
            )
        else:
            st.success(
                "Model Prediction: Negative"
            )
            st.write(
                "The model predicts the negative class."
            )

        # Confidence scores
        if probabilities is not None:

            classes = list(model.classes_)

            prediction_index = classes.index(prediction)

            prediction_confidence = (
                probabilities[prediction_index] * 100
            )

            st.metric(
                "Predicted Class Probability",
                f"{prediction_confidence:.2f}%"
            )

            st.subheader("Class Probability Distribution")

            probability_df = pd.DataFrame({
                "Prediction Class": [
                    str(c) for c in classes
                ],
                "Probability (%)": probabilities * 100
            })

            st.bar_chart(
                probability_df.set_index("Prediction Class")
            )

            with st.expander("View detailed probabilities"):
                st.dataframe(
                    probability_df,
                    use_container_width=True,
                    hide_index=True
                )

        st.info(
            "This result represents a machine learning prediction only. "
            "It is not a medical diagnosis. Consult a qualified healthcare "
            "professional for medical assessment."
        )

    except Exception as e:
        st.error(f"Prediction failed: {e}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<div style="text-align:center; color:#52677F; padding:15px;">

<strong>Heart Disease Prediction System</strong><br>
Machine Learning | Python | Streamlit<br>
Educational and research purposes only

</div>
""", unsafe_allow_html=True)
