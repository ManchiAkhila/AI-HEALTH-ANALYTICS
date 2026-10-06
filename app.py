import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HealthMirror",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# FILE PATH
# ============================================================

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "health_data.csv"

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f7f4ed;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    color: #30483a !important;
}

h2 {
    color: #3d5949 !important;
}

h3 {
    color: #4b6656 !important;
}

p, label {
    color: #46544c !important;
}

[data-testid="stSidebar"] {
    background-color: #28332f;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: white !important;
}

[data-testid="stMetric"] {
    background-color: #fffdf8;
    border: 1px solid #e2ddd2;
    border-radius: 18px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #68746d !important;
}

[data-testid="stMetricValue"] {
    color: #385344 !important;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid #bdcbbd;
    background-color: white;
    color: #385344 !important;
    font-weight: 600;
    min-height: 45px;
}

.stButton > button:hover {
    background-color: #e8f0e5;
}

[data-testid="stForm"] {
    background-color: #fffdf8;
    border: 1px solid #e2ddd2;
    border-radius: 20px;
    padding: 25px;
}

.footer {
    text-align: center;
    color: #7b857d;
    padding: 30px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD CSV
# ============================================================

if not DATA_FILE.exists():
    st.error("❌ health_data.csv not found.")
    st.write("Expected file location:")
    st.code(str(DATA_FILE))
    st.write("Files found in this folder:")

    for file in BASE_DIR.iterdir():
        st.write("•", file.name)

    st.stop()

try:
    data = pd.read_csv(DATA_FILE)

except Exception as e:
    st.error("❌ Unable to read health_data.csv")
    st.exception(e)
    st.stop()

# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "date",
    "sleep_hours",
    "water_liters",
    "food_quality",
    "activity_minutes",
    "energy_level",
    "headache",
    "pain",
    "temperature",
    "heart_rate"
]

missing_columns = [
    col for col in required_columns
    if col not in data.columns
]

if missing_columns:
    st.error("❌ Missing columns in health_data.csv:")
    st.write(missing_columns)
    st.stop()

# ============================================================
# CLEAN DATA
# ============================================================

data["date"] = pd.to_datetime(
    data["date"],
    errors="coerce"
)

numeric_columns = [
    "sleep_hours",
    "water_liters",
    "food_quality",
    "activity_minutes",
    "energy_level",
    "headache",
    "pain",
    "temperature",
    "heart_rate"
]

for col in numeric_columns:
    data[col] = pd.to_numeric(
        data[col],
        errors="coerce"
    )

data = data.dropna(subset=["date"])

data = data.sort_values(
    "date"
).reset_index(drop=True)

if data.empty:
    st.error("❌ No valid health records found.")
    st.stop()

latest = data.iloc[-1]

# ============================================================
# BASELINE
# ============================================================

baseline = {
    "sleep_hours": data["sleep_hours"].mean(),
    "water_liters": data["water_liters"].mean(),
    "food_quality": data["food_quality"].mean(),
    "activity_minutes": data["activity_minutes"].mean(),
    "energy_level": data["energy_level"].mean(),
    "temperature": data["temperature"].mean(),
    "heart_rate": data["heart_rate"].mean()
}

# ============================================================
# PATTERN DETECTION
# ============================================================

score = 0
patterns = []

if latest["sleep_hours"] < baseline["sleep_hours"] - 1:
    score += 1
    patterns.append("Low sleep")

if latest["water_liters"] < baseline["water_liters"] - 0.5:
    score += 1
    patterns.append("Low water intake")

if latest["food_quality"] < baseline["food_quality"] - 2:
    score += 1
    patterns.append("Lower food quality")

if latest["activity_minutes"] < baseline["activity_minutes"] - 15:
    score += 1
    patterns.append("Low physical activity")

if latest["energy_level"] < baseline["energy_level"] - 2:
    score += 1
    patterns.append("Low energy")

if latest["temperature"] > baseline["temperature"] + 0.5:
    score += 1
    patterns.append("Higher temperature")

if latest["heart_rate"] > baseline["heart_rate"] + 15:
    score += 1
    patterns.append("Higher heart rate")

if latest["headache"] == 1:
    score += 1
    patterns.append("Headache")

if latest["pain"] > 0:
    score += 1
    patterns.append("Pain")

# ============================================================
# STATUS
# ============================================================

if score == 0:
    status = "Normal"
elif score <= 2:
    status = "Slight change detected"
elif score <= 4:
    status = "Multiple changes detected"
else:
    status = "Significant change detected"

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("❤️ HealthMirror")

    st.caption(
        "Personalized Healthcare Companion"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📝 Daily Check-In",
            "🩺 Find Specialist",
            "🌐 Language Translator",
            "📄 Doctor Report",
            "📹 Consultation"
        ]
    )

    st.divider()

    elderly_mode = st.checkbox(
        "👵 Enable Elderly Mode"
    )

    st.divider()

    st.caption(
        "HealthMirror does not diagnose diseases "
        "or replace professional medical advice."
    )

# ============================================================
# ELDERLY MODE
# ============================================================

if elderly_mode:

    st.info(
        "👵 Elderly Mode is ON. "
        "Options are displayed in a simpler format."
    )

# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title("❤️ HealthMirror")

    st.subheader(
        "AI-Based Personalized Health Monitoring & Healthcare Navigation"
    )

    st.write(
        "HealthMirror learns your personal health baseline, "
        "detects meaningful changes over time and helps "
        "users navigate healthcare services."
    )

    st.success(
        "Latest record: "
        + latest["date"].strftime("%d %B %Y")
    )

    st.divider()

    st.header("📊 Personal Health Baseline")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "💤 Sleep",
            f"{baseline['sleep_hours']:.1f} hrs"
        )

    with c2:
        st.metric(
            "💧 Water",
            f"{baseline['water_liters']:.2f} L"
        )

    with c3:
        st.metric(
            "⚡ Energy",
            f"{baseline['energy_level']:.1f}/10"
        )

    with c4:
        st.metric(
            "❤️ Heart Rate",
            f"{baseline['heart_rate']:.1f} bpm"
        )

    st.divider()

    st.header("🔎 Health Pattern Analysis")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Pattern Score",
            score
        )

    with c2:
        st.metric(
            "Current Status",
            status
        )

    if score == 0:
        st.success(
            "💚 Your latest health record is close to "
            "your personal baseline."
        )

    elif score <= 2:
        st.warning(
            "🟡 A small change from your usual pattern "
            "was detected."
        )

    elif score <= 4:
        st.warning(
            "🟠 Multiple changes from your personal "
            "baseline were detected."
        )

    else:
        st.error(
            "🔴 Several significant changes were detected."
        )

    st.subheader("Detected Changes")

    if patterns:

        for item in patterns:
            st.warning("• " + item)

    else:
        st.success("✓ No unusual changes detected.")

    st.header("💡 Personalized Health Insight")

    if score == 0:

        st.info(
            "Your latest health record is close to your "
            "personal baseline. Continue monitoring your "
            "daily health habits."
        )

    elif score <= 2:

        st.info(
            "A small change was detected. Continue tracking "
            "your health over the next few days."
        )

    elif score <= 4:

        st.warning(
            "Multiple changes were detected. Continue "
            "tracking your health and consider discussing "
            "persistent changes with a healthcare professional."
        )

    else:

        st.warning(
            "Several changes were detected. If these changes "
            "persist or you feel unwell, seek professional "
            "medical advice."
        )

    st.divider()

    st.header("📈 Health Trends")

    chart_data = data.set_index("date")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("💤 Sleep")
        st.line_chart(
            chart_data["sleep_hours"]
        )

    with c2:
        st.subheader("💧 Water")
        st.line_chart(
            chart_data["water_liters"]
        )

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("⚡ Energy")
        st.line_chart(
            chart_data["energy_level"]
        )

    with c2:
        st.subheader("❤️ Heart Rate")
        st.line_chart(
            chart_data["heart_rate"]
        )

    st.divider()

    st.header("📋 Health History")

    display_data = data.copy()

    display_data["date"] = display_data[
        "date"
    ].dt.strftime("%d %b %Y")

    st.dataframe(
        display_data.tail(10),
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# DAILY CHECK-IN
# ============================================================

elif page == "📝 Daily Check-In":

    st.title("📝 Daily Health Check-In")

    st.write(
        "Enter today's health information."
    )

    with st.form("health_form"):

        sleep = st.number_input(
            "💤 Sleep (hours)",
            0.0,
            24.0,
            7.0,
            0.5
        )

        water = st.number_input(
            "💧 Water intake (liters)",
            0.0,
            10.0,
            2.0,
            0.1
        )

        food = st.slider(
            "🍎 Food quality",
            0,
            10,
            7
        )

        activity = st.number_input(
            "🏃 Activity (minutes)",
            0,
            500,
            30
        )

        energy = st.slider(
            "⚡ Energy level",
            0,
            10,
            7
        )

        headache = st.checkbox(
            "🤕 Headache"
        )

        pain = st.slider(
            "🩹 Pain level",
            0,
            10,
            0
        )

        temperature = st.number_input(
            "🌡️ Temperature (°C)",
            30.0,
            45.0,
            36.7,
            0.1
        )

        heart_rate = st.number_input(
            "❤️ Heart rate",
            30,
            220,
            75
        )

        submitted = st.form_submit_button(
            "Save Today's Health Data"
        )

    if submitted:

        new_row = pd.DataFrame([{
            "date": str(date.today()),
            "sleep_hours": sleep,
            "water_liters": water,
            "food_quality": food,
            "activity_minutes": activity,
            "energy_level": energy,
            "headache": int(headache),
            "pain": pain,
            "temperature": temperature,
            "heart_rate": heart_rate
        }])

        try:

            new_row.to_csv(
                DATA_FILE,
                mode="a",
                header=False,
                index=False
            )

            st.success(
                "✅ Today's health data was saved."
            )

            st.rerun()

        except Exception as e:

            st.error(
                "❌ Could not save the health data."
            )

            st.exception(e)

# ============================================================
# FIND SPECIALIST
# ============================================================

elif page == "🩺 Find Specialist":

    st.title("🩺 Find the Right Specialist")

    st.write(
        "HealthMirror suggests healthcare specialties "
        "based on recorded patterns."
    )

    st.info(
        "This is healthcare navigation, not a diagnosis."
    )

    recommendations = []

    if latest["headache"] == 1:

        recommendations.append(
            (
                "Neurologist",
                "Neurology",
                "For persistent headaches or neurological symptoms."
            )
        )

    if latest["heart_rate"] > baseline["heart_rate"] + 10:

        recommendations.append(
            (
                "Cardiologist",
                "Cardiology",
                "For persistent heart-rate or cardiovascular concerns."
            )
        )

    if latest["pain"] > 0:

        recommendations.append(
            (
                "Orthopedist",
                "Orthopedics",
                "For persistent bone, joint or muscle pain."
            )
        )

    if latest["sleep_hours"] < baseline["sleep_hours"] - 1:

        recommendations.append(
            (
                "Sleep Specialist",
                "Sleep Medicine",
                "For persistent sleep-related concerns."
            )
        )

    if latest["energy_level"] < baseline["energy_level"] - 2:

        recommendations.append(
            (
                "General Physician",
                "General Medicine",
                "For an overall health assessment."
            )
        )

    if not recommendations:

        recommendations.append(
            (
                "General Physician",
                "General Medicine",
                "Useful for routine health evaluation."
            )
        )

    st.subheader("Recommended Specialists")

    for name, specialty, reason in recommendations:

        st.markdown(
            f"### 🩺 {name}"
        )

        st.write(
            f"**Specialty:** {specialty}"
        )

        st.write(
            f"**Why:** {reason}"
        )

        st.divider()

    st.header("🌍 Search Specialists Worldwide")

    country = st.selectbox(
        "Country",
        [
            "India",
            "United States",
            "United Kingdom",
            "Germany",
            "Canada",
            "Australia",
            "Singapore",
            "United Arab Emirates",
            "France",
            "Japan"
        ]
    )

    city = st.text_input(
        "City / Location",
        placeholder="Example: Hyderabad"
    )

    specialty = st.selectbox(
        "Specialist",
        [
            "General Physician",
            "Neurologist",
            "Cardiologist",
            "Dermatologist",
            "Gastroenterologist",
            "Orthopedist",
            "Endocrinologist",
            "ENT Specialist",
            "Ophthalmologist",
            "Nephrologist",
            "Urologist",
            "Gynecologist",
            "Pediatrician",
            "Psychiatrist",
            "Psychologist",
            "Sleep Specialist"
        ]
    )

    consultation = st.radio(
        "Consultation type",
        ["Online", "In-Person"],
        horizontal=True
    )

    if st.button("🔎 Search Specialists"):

        location = city.strip() or country

        st.success(
            f"{specialty} search created for "
            f"{location} ({consultation})."
        )

        st.info(
            "A real doctor-directory or telemedicine "
            "API can be connected here."
        )

# ============================================================
# LANGUAGE TRANSLATOR
# ============================================================

elif page == "🌐 Language Translator":

    st.title("🌐 Healthcare Language Translator")

    st.write(
        "Translate health information between different languages."
    )

    st.info(
        "Medical translations should be verified by a qualified "
        "interpreter or healthcare professional when important."
    )

    languages = [
        "English",
        "Telugu",
        "Hindi",
        "Tamil",
        "Kannada",
        "Malayalam",
        "Marathi",
        "Bengali",
        "Spanish",
        "French",
        "German",
        "Arabic",
        "Japanese"
    ]

    c1, c2 = st.columns(2)

    with c1:

        source = st.selectbox(
            "From",
            languages
        )

    with c2:

        target = st.selectbox(
            "To",
            languages,
            index=1
        )

    text = st.text_area(
        "Enter your health message",
        height=160,
        placeholder="Example: I have been having headaches for three days."
    )

    if st.button("🌐 Translate"):

        if not text.strip():

            st.warning(
                "Please enter a message."
            )

        elif source == target:

            st.info(
                "Both languages are the same."
            )

        else:

            st.success(
                f"Translation requested: {source} → {target}"
            )

            st.info(
                "AI translation can be connected here using "
                "a translation API."
            )

    st.divider()

    st.header("🎙️ Voice Translation")

    c1, c2 = st.columns(2)

    with c1:
        st.info(
            "🎤 Patient speaks in their preferred language."
        )

    with c2:
        st.info(
            "🗣️ HealthMirror converts the communication "
            "for the healthcare professional."
        )

# ============================================================
# DOCTOR REPORT
# ============================================================

elif page == "📄 Doctor Report":

    st.title("📄 Doctor Health Report")

    if patterns:

        detected = "\n".join(
            "- " + p
            for p in patterns
        )

    else:

        detected = "- No unusual changes detected."

    report = f"""
HEALTHMIRROR
DOCTOR HEALTH REPORT

Generated: {date.today()}

PERSONAL HEALTH BASELINE

Average Sleep: {baseline['sleep_hours']:.2f} hours
Average Water: {baseline['water_liters']:.2f} liters
Average Food Quality: {baseline['food_quality']:.2f}/10
Average Activity: {baseline['activity_minutes']:.2f} minutes
Average Energy: {baseline['energy_level']:.2f}/10
Average Temperature: {baseline['temperature']:.2f} °C
Average Heart Rate: {baseline['heart_rate']:.2f} bpm

LATEST RECORD

Date: {latest['date'].strftime("%d %B %Y")}
Sleep: {latest['sleep_hours']} hours
Water: {latest['water_liters']} liters
Food Quality: {latest['food_quality']}/10
Activity: {latest['activity_minutes']} minutes
Energy: {latest['energy_level']}/10
Headache: {"Yes" if latest['headache'] else "No"}
Pain: {latest['pain']}/10
Temperature: {latest['temperature']} °C
Heart Rate: {latest['heart_rate']} bpm

PATTERN ANALYSIS

Pattern Score: {score}
Status: {status}

Detected Changes:

{detected}

IMPORTANT NOTICE

This report is intended for healthcare support
and communication.

It is NOT a medical diagnosis.
"""

    st.text_area(
        "Report Preview",
        report,
        height=550
    )

    st.download_button(
        "📥 Download Doctor Report",
        data=report,
        file_name="HealthMirror_Doctor_Report.txt",
        mime="text/plain"
    )

# ============================================================
# CONSULTATION
# ============================================================

elif page == "📹 Consultation":

    st.title("📹 Healthcare Consultation")

    st.write(
        "HealthMirror can be connected to secure "
        "telemedicine services."
    )

    st.warning(
        "These are prototype interfaces. "
        "A secure telemedicine provider must be integrated "
        "before real patient-doctor calls."
    )

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("📹 Video Consultation")

        if st.button("Start Video Consultation"):

            st.info(
                "Video consultation service will be connected here."
            )

    with c2:

        st.subheader("📞 Audio Consultation")

        if st.button("Start Audio Consultation"):

            st.info(
                "Audio consultation service will be connected here."
            )

    st.divider()

    share = st.checkbox(
        "Allow doctor to view my HealthMirror report"
    )

    if share:

        st.success(
            "Your report is ready to be shared."
        )

        st.dataframe(
            data.tail(10),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Your health information is not shared until "
            "you give permission."
        )

# ============================================================
# SAFETY NOTICE
# ============================================================

st.divider()

st.warning(
    "❤️ HealthMirror is designed for health monitoring, "
    "pattern awareness and healthcare navigation. "
    "It does not diagnose diseases, prescribe medicines "
    "or replace professional medical advice."
)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
❤️ HealthMirror<br>
Personalized Health Monitoring & Healthcare Navigation<br><br>
Your health information should remain private,
secure and under your control.
</div>
""",
    unsafe_allow_html=True
)
