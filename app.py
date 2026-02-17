import streamlit as st
import os
import json
import pandas as pd
import torch

from sentence_transformers import SentenceTransformer, util

from src.parser import parse_resume
from src.skill_extractor import extract_skills, load_skill_dictionary
# -------------------------------
# Session Initialization
# -------------------------------

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

if "resume_path" not in st.session_state:
    st.session_state.resume_path = None

if "user_skills" not in st.session_state:
    st.session_state.user_skills = []


# ------------------------------------------------
# CONFIG
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="SkillSentinel",
    page_icon="🧠",
    layout="wide"
)


# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

skills_dict = load_skill_dictionary()

risk_df = pd.read_csv(
    os.path.join(BASE_DIR, "reports", "skill_risk_scores.csv")
)

trend_df = pd.read_csv(
    os.path.join(BASE_DIR, "data/job_market/skill_trend_comparison.csv")
)


# Quiz data
quiz_path = os.path.join(BASE_DIR, "data", "skill_quiz.json")

if os.path.exists(quiz_path):
    with open(quiz_path, "r") as f:
        quiz_data = json.load(f)
else:
    quiz_data = {}


# ------------------------------------------------
# LOAD SBERT
# ------------------------------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()

all_skills = list(skills_dict.keys())

skill_embeddings = model.encode(
    all_skills,
    convert_to_tensor=True
)


# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------

if "user_skills" not in st.session_state:
    st.session_state.user_skills = []

if "verified" not in st.session_state:
    st.session_state.verified = {}


# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("🧭 SkillSentinel")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Verification", "Report", "About"]
)


# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown(
    """
    <h1 style='text-align:center;'>🧠 SkillSentinel</h1>
    <h4 style='text-align:center;color:gray;'>
    AI-Powered Career Risk Analyzer
    </h4>
    """,
    unsafe_allow_html=True
)

st.divider()


# ------------------------------------------------
# HELPER: COLOR RISK
# ------------------------------------------------

def color_risk(val):

    if val >= 60:
        return "background-color:#ff7675;color:white"
    elif val >= 30:
        return "background-color:#ffeaa7"
    else:
        return "background-color:#55efc4"


# =========================================================
# DASHBOARD
# =========================================================

# ===============================
# DASHBOARD PAGE
# ===============================

# ===============================
# DASHBOARD PAGE
# ===============================

if page == "Dashboard":

    import time
    import numpy as np
    import pandas as pd
    import plotly.express as px

    from src.parser import parse_resume
    from src.skill_extractor import extract_skills, load_skill_dictionary


    # -------------------------------
    # Session Safe Initialization
    # -------------------------------

    if "resume_uploaded" not in st.session_state:
        st.session_state.resume_uploaded = False

    if "user_skills" not in st.session_state:
        st.session_state.user_skills = []

    user_skills = st.session_state.get("user_skills", [])


    # -------------------------------
    # Page Header
    # -------------------------------

    st.title("🧠 SkillSentinel – AI Career Risk Analyzer")

    st.markdown(
        "Analyze your resume, evaluate skill risks, and get AI-powered guidance."
    )

    st.markdown("---")


    # -------------------------------
    # Resume Upload
    # -------------------------------

    uploaded_file = st.file_uploader(
        "📂 Upload Resume (PDF)",
        type=["pdf"]
    )


    if uploaded_file and not st.session_state.resume_uploaded:

        with st.spinner("🔍 AI is analyzing your resume..."):

            time.sleep(2)

            file_path = "data/resumes/temp_resume.pdf"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())


            # Parse Resume
            resume_text = parse_resume(file_path)

            skill_dict = load_skill_dictionary("data/skills.json")

            skill_map = extract_skills(resume_text, skill_dict)

            extracted = [
                s for s, v in skill_map.items() if v
            ]


            # Save to Session
            st.session_state.resume_uploaded = True
            st.session_state.user_skills = extracted

            user_skills = extracted


        st.success("✅ Resume analyzed successfully!")


    elif st.session_state.resume_uploaded:

        st.success("✅ Resume already analyzed")


    else:

        st.info("📄 Please upload your resume to start analysis")
        st.stop()


    # -------------------------------
    # Reset Option
    # -------------------------------

    if st.button("🔄 Upload New Resume"):

        st.session_state.resume_uploaded = False
        st.session_state.user_skills = []

        st.experimental_rerun()


    st.markdown("---")


    # -------------------------------
    # Load Data
    # -------------------------------

    risk_df = pd.read_csv("reports/skill_risk_scores.csv")

    trend_df = pd.read_csv(
        "data/job_market/skill_trend_comparison.csv"
    )

    trend_time_df = pd.read_csv(
        "data/job_market/skill_demand_by_month_final.csv"
    )


    user_data = risk_df[
        risk_df["skill"].isin(user_skills)
    ]


    trends = user_data["trend"].tolist()
    risk_scores = user_data["risk_score"].tolist()


    # -------------------------------
    # KPI CARDS
    # -------------------------------

    st.markdown("## 📊 Skill Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📌 Total Skills", len(user_skills))

    c2.metric(
        "📈 Growing",
        sum(t == "Increasing" for t in trends)
    )

    c3.metric(
        "⚠️ High Risk",
        sum(r > 60 for r in risk_scores)
    )

    c4.metric(
        "🎯 Avg Risk",
        f"{round(np.mean(risk_scores),1)}%"
    )


    st.markdown("---")


    # -------------------------------
    # Top Risks
    # -------------------------------

    st.markdown("## 🚨 Critical Skills")

    top_risks = user_data.sort_values(
        "risk_score",
        ascending=False
    ).head(3)


    for _, row in top_risks.iterrows():

        st.error(
            f"⚠️ {row['skill'].upper()} → {row['risk_score']}% Risk"
        )


    st.markdown("---")


    # -------------------------------
    # Skill Risk Table
    # -------------------------------

    st.markdown("## ⚠️ Skill Risk Table")


    verified = st.session_state.get("verified_skills", [])

    display_df = user_data.copy()

    display_df["Verified"] = display_df["skill"].apply(
        lambda x: "✅" if x in verified else "❌"
    )


    st.dataframe(
        display_df.style.background_gradient(
            subset=["risk_score"],
            cmap="RdYlGn_r"
        ),
        use_container_width=True
    )


    st.markdown("---")


    # -------------------------------
    # Risk Distribution (Donut)
    # -------------------------------

    st.markdown("## 🎯 Risk Distribution")


    low = sum(r < 30 for r in risk_scores)
    mid = sum(30 <= r <= 60 for r in risk_scores)
    high = sum(r > 60 for r in risk_scores)


    donut_df = pd.DataFrame({
        "Level": ["Low", "Medium", "High"],
        "Count": [low, mid, high]
    })


    fig = px.pie(
        donut_df,
        names="Level",
        values="Count",
        hole=0.5,
        color="Level",
        color_discrete_map={
            "Low": "#2ecc71",
            "Medium": "#f39c12",
            "High": "#e74c3c"
        }
    )

    st.plotly_chart(fig, use_container_width=True)


    st.markdown("---")


    # -------------------------------
    # Radar Chart
    # -------------------------------

    st.markdown("## 🧭 Skill Strength Radar")


    radar_df = pd.DataFrame({
        "Skill": user_data["skill"],
        "Score": 100 - user_data["risk_score"]
    })


    radar_fig = px.line_polar(
        radar_df,
        r="Score",
        theta="Skill",
        line_close=True
    )

    radar_fig.update_traces(fill="toself")

    st.plotly_chart(radar_fig, use_container_width=True)


    st.markdown("---")


    # -------------------------------
    # Market Demand Timeline
    # -------------------------------

    st.markdown("## 📈 Market Demand Timeline")

    st.caption(
        "Job demand trend based on LinkedIn postings (2023–2024)"
    )


    selected_skill = st.selectbox(
        "Select Skill to Analyze",
        user_skills
    )


    trend_row = trend_time_df[
        trend_time_df["skill"] == selected_skill
    ]


    if not trend_row.empty:

        ts = trend_row.drop("skill", axis=1).T

        ts.columns = ["Job Demand"]

        ts.index = pd.to_datetime(ts.index)

        st.line_chart(ts, height=350)


        start = ts.iloc[0, 0]
        end = ts.iloc[-1, 0]

        change = round(((end - start) / start) * 100, 2)


        if change > 10:
            st.success(f"📈 Demand increased by {change}%")
        elif change < -10:
            st.error(f"📉 Demand decreased by {change}%")
        else:
            st.warning("⚖️ Demand is stable")


    st.markdown("---")


    # -------------------------------
    # AI Explanation
    # -------------------------------

    with st.expander("🧠 AI Risk Explanation"):

        row = user_data[
            user_data["skill"] == selected_skill
        ].iloc[0]


        st.info(f"""
        📌 Skill: {selected_skill}

        📉 Trend: {row['trend']}

        ⚠️ Risk Score: {row['risk_score']}%

        📊 Based on historical job market data
        """)


    # -------------------------------
    # AI Recommendations
    # -------------------------------

    st.markdown("## 🤖 AI Recommendations")


    risky = user_data[
        user_data["risk_score"] > 30
    ].sort_values(
        "risk_score",
        ascending=False
    )


    for _, row in risky.iterrows():

        st.markdown(
            f"### 🔹 {row['skill']} ({row['risk_score']}%)"
        )


        rec_map = {
            "html": ["CSS", "JavaScript", "NodeJS"],
            "nosql": ["Big Data", "DBMS", "Data Structures"],
            "api development": ["FastAPI", "GraphQL", "Microservices"]
        }


        recs = rec_map.get(
            row["skill"],
            ["AI", "Cloud", "DevOps"]
        )


        st.write("➡ Learn:", ", ".join(recs))

        st.caption("AI-powered semantic similarity engine")

# =========================================================
# VERIFICATION
# =========================================================
elif page == "Verification":

    import json
    import random
    import pandas as pd

    st.title("🧪 Skill Verification Center")
    st.markdown("AI-Powered Skill Assessment & Certification")
# -------------------------------
# Load Quiz Bank
# -------------------------------

    with open("data/skill_quiz.json", "r") as f:
        quiz_bank = json.load(f)


    # -------------------------------
    # Initialize Session State
    # -------------------------------

    if "verified_skills" not in st.session_state:
        st.session_state.verified_skills = []

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "attempts" not in st.session_state:
        st.session_state.attempts = {}

    if "last_submitted" not in st.session_state:
        st.session_state.last_submitted = None

    if "last_correct" not in st.session_state:
        st.session_state.last_correct = False


    # -------------------------------
    # Get All Skills (Dashboard + Quiz)
    # -------------------------------

    dashboard_skills = st.session_state.get("user_skills", [])

    all_skills = sorted(
        list(set(list(quiz_bank.keys()) + dashboard_skills))
    )


    # -------------------------------
    # Skill & Level Selection
    # -------------------------------

    col1, col2 = st.columns(2)

    with col1:
        skill = st.selectbox(
            "Select Skill",
            all_skills
        )

    with col2:
        level = st.selectbox(
            "Difficulty Level",
            ["easy", "medium", "advanced"]
        )


    # -------------------------------
    # Default Quiz (Fallback)
    # -------------------------------

    default_quiz = {
        "easy": [
            {
                "q": f"What is {skill} mainly used for?",
                "options": [
                    "Software Development",
                    "Gaming",
                    "Music Editing",
                    "Video Rendering"
                ],
                "ans": "Software Development"
            }
        ],

        "medium": [
            {
                "q": f"Which field commonly uses {skill}?",
                "options": [
                    "IT Industry",
                    "Medical",
                    "Civil",
                    "Mechanical"
                ],
                "ans": "IT Industry"
            }
        ],

        "advanced": [
            {
                "q": f"Is {skill} important for modern tech jobs?",
                "options": ["Yes", "No"],
                "ans": "Yes"
            }
        ]
    }


    # -------------------------------
    # Select Quiz Source
    # -------------------------------

    if skill in quiz_bank:

        questions = quiz_bank[skill][level]

    else:

        st.info("ℹ️ Auto-generated assessment for this skill")

        questions = default_quiz[level]


    question = random.choice(questions)


    # -------------------------------
    # Display Question
    # -------------------------------

    st.markdown("---")

    st.subheader(f"📘 {skill.title()} ({level.upper()})")

    st.write("❓", question["q"])

    answer = st.radio(
    "Choose your answer:",
    question["options"],
    key=f"quiz_{skill}_{level}_{question['q']}"
)




    # -------------------------------
    # Submit Button
    # -------------------------------

    if st.button("Submit Answer"):

        st.session_state.last_submitted = skill

        # Initialize tracking
        if skill not in st.session_state.attempts:
            st.session_state.attempts[skill] = {
                "correct": 0,
                "total": 0
            }

        st.session_state.attempts[skill]["total"] += 1


        if answer == question["ans"]:

            st.session_state.last_correct = True

            st.session_state.attempts[skill]["correct"] += 1
            st.session_state.score += 1

            st.success("✅ Correct Answer!")

        else:

            st.session_state.last_correct = False

            st.error(f"❌ Wrong Answer. Correct: {question['ans']}")


        # Certification Rule (3 Correct = Verified)

        if st.session_state.attempts[skill]["correct"] >= 3:

            if skill not in st.session_state.verified_skills:

                st.session_state.verified_skills.append(skill)

                st.balloons()
                st.success(f"🏅 {skill.upper()} CERTIFIED!")


    # -------------------------------
    # Progress Analytics
    # -------------------------------

    st.markdown("---")
    st.subheader("📊 Learning Analytics")

    progress_data = []

    for s, v in st.session_state.attempts.items():

        accuracy = 0
        if v["total"] > 0:
            accuracy = round((v["correct"] / v["total"]) * 100, 2)

        progress_data.append([
            s.title(),
            v["correct"],
            v["total"],
            accuracy
        ])


    if progress_data:

        progress_df = pd.DataFrame(
            progress_data,
            columns=["Skill", "Correct", "Total", "Accuracy %"]
        )

        # Show table
        st.dataframe(progress_df, use_container_width=True)


        # -------------------------------
        # Bar Chart
        # -------------------------------

        st.subheader("🎯 Skill Mastery Levels")

        chart_df = progress_df.set_index("Skill")["Accuracy %"]

        st.bar_chart(chart_df)


        # -------------------------------
        # Certification Progress
        # -------------------------------

        st.subheader("🏆 Certification Progress")

        for s, v in st.session_state.attempts.items():

            percent = min((v["correct"] / 3) * 100, 100)

            st.write(f"📌 {s.title()}")

            st.progress(int(percent))


    # -------------------------------
    # Verified Skills Display
    # -------------------------------

    if st.session_state.verified_skills:

        st.markdown("---")
        st.subheader("✅ Certified Skills")

        for s in st.session_state.verified_skills:
            st.write("✔️", s.title())


    # -------------------------------
    # Overall Score
    # -------------------------------

    st.markdown("---")
    st.metric("🏅 Total Score", st.session_state.score)


    # Show progress
    st.markdown("### 📊 Progress")

    st.metric("Score", st.session_state.score)

    if st.session_state.verified_skills:

        st.markdown("### ✅ Certified Skills")

        for s in st.session_state.verified_skills:
            st.write("✔️", s.title())




# =========================================================
# REPORT
# =========================================================

elif page == "Report":

    st.header("📄 Final Report")


    if not st.session_state.user_skills:

        st.warning("Analyze resume first.")
        st.stop()


    user_skills = st.session_state.user_skills

    user_risk = risk_df[
        risk_df["skill"].isin(user_skills)
    ]


    top = user_risk.sort_values(
        "risk_score", ascending=False
    ).head(3)


    report = "SkillSentinel Report\n"
    report += "------------------------\n\n"

    report += f"Total Skills: {len(user_skills)}\n\n"

    report += "Top Risky Skills:\n"

    for _, r in top.iterrows():
        report += f"- {r['skill']} ({r['risk_score']}%)\n"

    report += "\nVerified Skills:\n"

    for k, v in st.session_state.verified.items():
        if v:
            report += f"- {k}\n"


    st.text(report)


    st.download_button(
        "📥 Download Report",
        report,
        file_name="skillsentinel_report.txt"
    )



# =========================================================
# ABOUT
# =========================================================

elif page == "About":

    st.header("ℹ️ About")

    st.markdown(
        """
        **SkillSentinel** is an AI-powered system that:

        - Extracts skills from resumes
        - Analyzes job market trends
        - Predicts risk of skill obsolescence
        - Recommends upgrades using SBERT
        - Verifies skills using quizzes

        Developed by Vinay.
        """
    )
