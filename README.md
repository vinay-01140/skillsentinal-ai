🧠 SkillSentinel – AI-Powered Career Skill Risk Analyzer

SkillSentinel is an intelligent resume analysis and career guidance system that evaluates a user’s technical skills against real job market trends and predicts future skill risks using Artificial Intelligence and data analytics.

The system helps students and professionals identify outdated or risky skills and provides personalized upskilling recommendations using semantic similarity models.

📌 Project Motivation

With rapid technological evolution, many professional skills become obsolete within a few years. Students and early-career professionals often lack reliable tools to evaluate whether their current skillset aligns with future industry demand.

SkillSentinel addresses this problem by:

Analyzing real job market data

Detecting skill demand trends

Computing personalized risk scores

Recommending future-ready skills

Verifying knowledge through quizzes

This enables users to make informed career decisions.

🎯 Objectives

Extract skills automatically from resumes

Analyze historical job market demand

Identify declining and growing skills

Compute personalized skill risk scores

Recommend related micro-skills using AI

Provide explainable insights

Verify skills using automated quizzes

Generate professional reports

🏗️ System Architecture
Resume → Skill Extraction → Trend Analysis → Risk Engine → AI Recommendation → Verification → Report

Components:

Resume Parser

Skill Extractor

Job Market Processor

Trend Analyzer

Risk Engine

SBERT Recommendation Engine

Verification Module

Streamlit Dashboard

SKILLSENTINEL-AI/
│
├── data/
│   ├── job_market/          # Raw datasets (excluded from repo if large)
│   ├── resumes/             # Resume PDFs
│   ├── skill_quiz.json
│   ├── skill_metadata.json
│   └── user_experience.json
│
├── reports/
│   ├── skill_risk_scores.csv
│   └── skill_demand_trends.png
│
├── src/
│   ├── app.py
│   ├── parser.py
│   ├── skill_extractor.py
│   ├── trend_analysis.py
│   ├── risk_engine.py
│   ├── sbert_recommender.py
│   ├── recommender.py
│   └── verifier.py
│
├── requirements.txt
└── README.md

⚙️ Technologies Used
Category	                Technology
Language	                Python 3.13
UI	                        Streamlit
Data Processing	            Pandas, NumPy
AI / NLP	                Sentence-BERT, Transformers
Machine Learning	        Scikit-learn
Resume Parsing	            PDFPlumber
Visualization	            Matplotlib, Streamlit Charts
Model Framework	            PyTorch
Version Control	            Git, GitHub

🧠 AI Techniques Used

1️⃣ Skill Extraction

Rule-based matching using alias dictionaries

Resume text preprocessing

2️⃣ Trend Analysis

Time-series aggregation

Rolling averages

Percentage change analysis

3️⃣ Risk Modeling

Weighted formula combining:

Market trend

Skill age

User experience

Risk = 0.5 × Trend + 0.3 × Age + 0.2 × Experience

4️⃣ Semantic Similarity (SBERT)

Pretrained model: all-MiniLM-L6-v2

Cosine similarity for skill recommendations

Embedding-based matching

5️⃣ Explainable AI

Generates human-readable explanations

Highlights risk factors clearly

📊 Data Sources

LinkedIn Job Postings Dataset

Kaggle Job Market Datasets

Skill Mapping Datasets

All data is cleaned, validated, and aggregated before analysis.

🖥️ Features
Dashboard

Resume upload
    
Extracted skills view
    
Risk table
    
Trend visualization
    
AI recommendations
    
Verification
    
Skill-based quizzes
    
Difficulty levels
    
Auto-grading
    
Verified badge system
    
Reporting
    
Downloadable reports
    
Risk summaries
    
Personalized guidance

🚀 Installation & Setup
Step 1: Clone Repository
git clone https://github.com/your-username/skillsentinel-ai.git
cd skillsentinel-ai

Step 2: Create Virtual Environment
python -m venv venv
venv\Scripts\activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Run Application
streamlit run app.py

📈 Usage Workflow

Upload resume
    |
Extract skills automatically
    |
View risk dashboard
    |
Analyze market trends
    |
Get AI recommendations
    |
Complete verification quizzes
    |
Download final report

⚠️ Challenges Faced & Solutions

Challenge	                    Solution
Noisy job data	                Data cleaning pipelines
Inconsistent skill names	    Skill alias mapping
Missing time-series data	    Data reconstruction
UI state loss	                Session management
JSON parsing errors	            Validation checks
SBERT loading issues	        Dependency fixes
Verification mismatch	        Skill mapping

🧪 Testing & Validation

Manual testing on multiple resumes

Dataset validation reports

Risk score calibration

UI usability testing

Recommendation accuracy checks

📌 Results

Accurate detection of high-risk skills

Meaningful AI recommendations

Explainable outputs

Interactive dashboard

Stable verification system

The system successfully identifies outdated skills and suggests future-ready alternatives.

🔮 Future Enhancements

Cloud deployment

User authentication

Mobile interface

Live job API integration

Deep learning forecasting

Personalized learning paths

Industry-specific models

👨‍💻 Author

Vinay
B.Tech CSE (AI & ML)
Anil Neerukonda Institute of Technology and Sciences

Project developed for academic research, internship applications, and AI portfolio.

📜 License

This project is intended for educational and research purposes only.
