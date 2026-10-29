import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="HeartCare | Prediction",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: #f4f7fb;
}

.block-container {
    padding: 1rem 4%;
    max-width: 1200px;
}

.main-card {
    background: white;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

.hero {
    background: linear-gradient(120deg, #102a43, #176b87);
    color: white;
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: clamp(26px, 4vw, 40px);
    margin-bottom: 10px;
}

.hero p {
    color: #d9edf7;
    font-size: 16px;
}

.field-label {
    font-weight: 600;
    color: #243b53;
    margin: 12px 0 5px;
}

.metric {
    display: inline-block;
    width: 30%;
    min-width: 140px;
    background: #eef6fa;
    padding: 18px;
    margin: 5px 1%;
    border-radius: 12px;
    box-sizing: border-box;
}

.metric h3 {
    color: #176b87;
    margin: 0;
}

.metric p {
    color: #486581;
    margin-bottom: 0;
}

.footer {
    text-align: center;
    color: #627d98;
    padding: 20px;
    font-size: 13px;
}

@media (max-width: 600px) {
    .block-container {
        padding: 0.5rem 4%;
    }

    .hero, .main-card {
        padding: 18px;
        border-radius: 12px;
    }

    .metric {
        display: block;
        width: 100%;
        margin: 10px 0;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>HeartCare</h1>
    <p>Heart Disease Prediction & Risk Assessment</p>
    <p>Enter health measurements to explore a machine learning prediction.</p>
</div>

<div class="main-card">
    <h2>Patient Information</h2>
    <p>Provide the following measurements.</p>
</div>
""", unsafe_allow_html=True)

# Native Streamlit inputs remain accessible and interactive.
# HTML/CSS provides the visual styling and responsive page design.

st.markdown('<p class="field-label">Age</p>', unsafe_allow_html=True)
age = st.number_input("Age (years)", min_value=1, max_value=120, value=45)

st.markdown('<p class="field-label">Resting Blood Pressure</p>', unsafe_allow_html=True)
trestbps = st.number_input(
    "Resting blood pressure (mm Hg)",
    min_value=50, max_value=250, value=120
)

st.markdown('<p class="field-label">Cholesterol</p>', unsafe_allow_html=True)
chol = st.number_input(
    "Cholesterol (mg/dl)",
    min_value=50, max_value=700, value=200
)

st.markdown('<p class="field-label">Maximum Heart Rate</p>', unsafe_allow_html=True)
thalach = st.number_input(
    "Maximum heart rate achieved",
    min_value=40, max_value=250, value=150
)

st.markdown('<p class="field-label">Oldpeak</p>', unsafe_allow_html=True)
oldpeak = st.number_input(
    "ST depression (oldpeak)",
    min_value=0.0, max_value=10.0, value=1.0, step=0.1
)

if st.button("Analyze Measurements", use_container_width=True):
    st.markdown("""
    <div class="main-card">
        <h3>Measurements Received</h3>
        <p>Your inputs are ready for model integration.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric">
        <h3>{age}</h3>
        <p>Age (years)</p>
    </div>
    <div class="metric">
        <h3>{trestbps}</h3>
        <p>Blood pressure</p>
    </div>
    <div class="metric">
        <h3>{chol}</h3>
        <p>Cholesterol</p>
    </div>
    """, unsafe_allow_html=True)

    st.write({
        "age": age,
        "trestbps": trestbps,
        "chol": chol,
        "thalach": thalach,
        "oldpeak": oldpeak
    })

    st.info(
        "This UI currently demonstrates data entry only. "
        "Connect your trained model to generate predictions."
    )

st.markdown("""
<div class="footer">
    HeartCare ML Project · Educational Prototype<br>
    Not intended for medical diagnosis.
</div>
""", unsafe_allow_html=True)