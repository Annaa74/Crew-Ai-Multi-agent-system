"""
Streamlit UI for the AI Hiring Assistant
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Hiring Assistant",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
    }
    .metric-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        border-left: 4px solid #FF5733;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "api_url" not in st.session_state:
    st.session_state.api_url = os.getenv("API_URL", "http://localhost:8000")

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# Header
st.title("🤖 AI Hiring Assistant")
st.markdown("### Powered by CrewAI - Intelligent Job & Resume Analysis")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_url = st.text_input(
        "API URL",
        value=st.session_state.api_url,
        help="URL of the FastAPI backend"
    )
    st.session_state.api_url = api_url
    
    # Check API health
    if st.button("🔍 Check API Health", use_container_width=True):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ API is healthy!")
                health_data = response.json()
                st.json(health_data)
            else:
                st.error("❌ API returned an error")
        except Exception as e:
            st.error(f"❌ Cannot connect to API: {str(e)}")
    
    st.divider()
    
    # Stats
    if st.button("📊 View Database Stats", use_container_width=True):
        try:
            response = requests.get(f"{api_url}/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                st.json(stats)
            else:
                st.error("Could not retrieve stats")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.divider()
    
    # Analysis history
    st.header("📜 Analysis History")
    if st.button("Clear History", use_container_width=True):
        st.session_state.analysis_history = []
        st.success("History cleared!")


# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["📝 Job Analysis", "📄 Resume Analysis", "🎯 Full Hiring Analysis", "📊 Match Search"]
)

# ==================== TAB 1: Job Analysis ====================
with tab1:
    st.header("📝 Job Description Analysis")
    st.markdown("Extract key requirements from a job description")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        job_id = st.text_input("Job ID", value="JOB-001", key="tab1_job_id")
        job_title = st.text_input("Job Title", value="Senior Software Engineer", key="tab1_job_title")
    
    with col2:
        job_text = st.text_area(
            "Job Description",
            height=250,
            key="tab1_job_text",
            value="""Looking for a Senior Software Engineer with 5+ years of experience.
            
Required Skills:
- Python, JavaScript, TypeScript
- Docker, Kubernetes
- AWS/GCP/Azure
- PostgreSQL, MongoDB
- React, FastAPI

Responsibilities:
- Design and implement scalable backend systems
- Mentor junior engineers
- Code reviews and architecture decisions
- Collaborate with product team

Nice to have:
- Machine Learning experience
- Open source contributions
- DevOps experience"""
        )
    
    if st.button("🔍 Analyze Job Description", use_container_width=True):
        with st.spinner("Analyzing job description..."):
            try:
                response = requests.post(
                    f"{st.session_state.api_url}/api/v1/jobs/analyze",
                    json={
                        "job_id": job_id,
                        "job_title": job_title,
                        "job_text": job_text
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Job analysis completed!")
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    analysis = result.get("analysis", {})
                    
                    with col1:
                        st.metric("Required Skills", len(analysis.get("required_skills", [])))
                    with col2:
                        st.metric("Min Experience", f"{analysis.get('minimum_experience_years', 0)}+ years")
                    with col3:
                        st.metric("Job Title", result.get("job_title", "N/A"))
                    
                    # Detailed analysis
                    st.subheader("Detailed Analysis")
                    
                    tab_skills, tab_exp, tab_details = st.tabs(["Skills", "Experience", "Details"])
                    
                    with tab_skills:
                        skills = analysis.get("required_skills", [])
                        st.write(f"**Total Skills Required:** {len(skills)}")
                        cols = st.columns(3)
                        for i, skill in enumerate(skills):
                            with cols[i % 3]:
                                st.tag(skill)
                    
                    with tab_exp:
                        exp = analysis.get("minimum_experience_years", 0)
                        st.write(f"**Minimum Experience:** {exp} years")
                    
                    with tab_details:
                        st.json(analysis)
                    
                    # Save to history
                    st.session_state.analysis_history.append({
                        "type": "Job Analysis",
                        "job_id": job_id,
                        "timestamp": datetime.now().isoformat(),
                        "job_title": job_title
                    })
                    
                else:
                    st.error(f"API error: {response.status_code}")
                    st.write(response.json())
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ==================== TAB 2: Resume Analysis ====================
with tab2:
    st.header("📄 Resume Analysis & Optimization")
    st.markdown("Analyze resume quality and get optimization suggestions")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        resume_id = st.text_input("Resume ID", value="RES-001", key="tab2_resume_id")
        candidate_name = st.text_input("Candidate Name", value="John Doe", key="tab2_candidate_name")
    
    with col2:
        resume_text = st.text_area(
            "Resume Content",
            height=250,
            key="tab2_resume_text",
            value="""JOHN DOE | john@example.com | +1-234-567-8900

SUMMARY
Senior Software Engineer with 7 years of experience in full-stack development,
cloud architecture, and team leadership.

SKILLS
Technical: Python, JavaScript, TypeScript, Java
Frameworks: Django, FastAPI, React, Vue.js
Cloud: AWS (EC2, S3, Lambda), GCP (Compute Engine, Cloud Storage)
Databases: PostgreSQL, MongoDB, Redis
DevOps: Docker, Kubernetes, CI/CD pipelines

EXPERIENCE
Senior Software Engineer | Tech Company | 2021-Present
- Led development of microservices architecture serving 1M+ users
- Mentored team of 5 junior engineers
- Improved application performance by 40%

Software Engineer | Startup | 2018-2021
- Full-stack development using Python and React
- Implemented GraphQL API serving 100k+ requests/day
- Collaborated with product team on feature delivery

EDUCATION
BS Computer Science | State University | 2016"""
        )
    
    if st.button("🔍 Analyze Resume", use_container_width=True):
        with st.spinner("Analyzing resume..."):
            try:
                response = requests.post(
                    f"{st.session_state.api_url}/api/v1/resumes/analyze",
                    json={
                        "resume_id": resume_id,
                        "candidate_name": candidate_name,
                        "resume_text": resume_text
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Resume analysis completed!")
                    
                    # Display score
                    analysis = result.get("analysis", {})
                    score = analysis.get("optimization_score", 0)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Optimization Score", f"{score}/100")
                    with col2:
                        st.metric("Suggestions", analysis.get("total_suggestions", 0))
                    with col3:
                        st.metric("Candidate", result.get("candidate_name", "N/A"))
                    
                    # Detailed suggestions
                    st.subheader("Optimization Suggestions")
                    
                    priority_improvements = analysis.get("priority_improvements", [])
                    if priority_improvements:
                        st.write("### 🔴 Priority Improvements")
                        for i, imp in enumerate(priority_improvements, 1):
                            with st.expander(f"{i}. {imp.get('type', 'N/A')} - {imp.get('priority', 'N/A')}"):
                                st.write(f"**Suggestion:** {imp.get('suggestion', 'N/A')}")
                                st.write(f"**Impact:** {imp.get('impact', 'N/A')}")
                    
                    # Additional suggestions
                    additional = analysis.get("additional_suggestions", [])
                    if additional:
                        st.write("### ℹ️ Additional Suggestions")
                        for i, sugg in enumerate(additional, 1):
                            with st.expander(f"{i}. {sugg.get('type', 'N/A')} - {sugg.get('priority', 'N/A')}"):
                                st.write(f"**Suggestion:** {sugg.get('suggestion', 'N/A')}")
                                st.write(f"**Impact:** {sugg.get('impact', 'N/A')}")
                    
                    st.session_state.analysis_history.append({
                        "type": "Resume Analysis",
                        "resume_id": resume_id,
                        "timestamp": datetime.now().isoformat(),
                        "candidate": candidate_name
                    })
                    
                else:
                    st.error(f"API error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ==================== TAB 3: Full Hiring Analysis ====================
with tab3:
    st.header("🎯 Complete Hiring Analysis")
    st.markdown("Analyze job and resume together with match scoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Job Details")
        job_id_tab3 = st.text_input("Job ID", value="JOB-001", key="tab3_job_id")
        job_title_tab3 = st.text_input("Job Title", value="Senior Software Engineer", key="tab3_job_title")
        job_text_tab3 = st.text_area("Job Description", height=200, key="tab3_job_text")
    
    with col2:
        st.subheader("📄 Resume Details")
        resume_id_tab3 = st.text_input("Resume ID", value="RES-001", key="tab3_resume_id")
        candidate_name_tab3 = st.text_input("Candidate Name", value="John Doe", key="tab3_candidate_name")
        resume_text_tab3 = st.text_area("Resume Content", height=200, key="tab3_resume_text")
    
    st.divider()
    
    if st.button("🚀 Perform Full Hiring Analysis", use_container_width=True):
        with st.spinner("Analyzing job and resume..."):
            try:
                response = requests.post(
                    f"{st.session_state.api_url}/api/v1/hiring/analyze",
                    json={
                        "job": {
                            "job_id": job_id_tab3,
                            "job_title": job_title_tab3,
                            "job_text": job_text_tab3
                        },
                        "resume": {
                            "resume_id": resume_id_tab3,
                            "candidate_name": candidate_name_tab3,
                            "resume_text": resume_text_tab3
                        }
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Complete analysis finished!")
                    
                    # Display match score prominently
                    match_score = result.get("match_score", 0)
                    recommendation = result.get("recommendation", "UNKNOWN")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Match Score",
                            f"{match_score:.1f}%",
                            delta="Excellent" if match_score >= 75 else "Good" if match_score >= 60 else "Fair"
                        )
                    with col2:
                        st.metric("Recommendation", recommendation)
                    with col3:
                        st.metric("Job", job_title_tab3)
                    with col4:
                        st.metric("Candidate", candidate_name_tab3)
                    
                    st.divider()
                    
                    # Detailed analysis
                    tab_jd, tab_resume = st.tabs(["Job Analysis", "Resume Analysis"])
                    
                    with tab_jd:
                        st.subheader("Job Description Analysis")
                        jd_analysis = result.get("jd_analysis", {})
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Required Skills", len(jd_analysis.get("required_skills", [])))
                        with col2:
                            st.metric("Min Experience", f"{jd_analysis.get('minimum_experience_years', 0)}+ yrs")
                        with col3:
                            st.metric("Skill Density", f"{len(jd_analysis.get('required_skills', []))} unique")
                        
                        st.json(jd_analysis)
                    
                    with tab_resume:
                        st.subheader("Resume Analysis")
                        resume_analysis = result.get("resume_analysis", {})
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Skill Match", f"{resume_analysis.get('skill_match_percentage', 0):.1f}%")
                        with col2:
                            st.metric("Matched Skills", len(resume_analysis.get("matched_skills", [])))
                        with col3:
                            st.metric("Missing Skills", len(resume_analysis.get("missing_skills", [])))
                        
                        st.json(resume_analysis)
                    
                    st.session_state.analysis_history.append({
                        "type": "Full Hiring Analysis",
                        "job_id": job_id_tab3,
                        "resume_id": resume_id_tab3,
                        "timestamp": datetime.now().isoformat(),
                        "match_score": match_score,
                        "recommendation": recommendation
                    })
                    
                else:
                    st.error(f"API error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ==================== TAB 4: Match Search ====================
with tab4:
    st.header("📊 Vector Database Search & Matching")
    st.markdown("Find matching resumes for jobs or jobs for resumes")
    
    search_type = st.radio("Search Type", ["Find Resumes for Job", "Find Jobs for Resume"], key="tab4_search_type")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if search_type == "Find Resumes for Job":
            job_id_tab4 = st.text_input("Job ID", value="JOB-001", key="tab4_job_id")
            search_text = st.text_area(
                "Job Description",
                height=150,
                key="tab4_search_text_job",
                value="Senior Software Engineer with 5+ years experience in Python, JavaScript, and cloud platforms"
            )
        else:
            resume_id_tab4 = st.text_input("Resume ID", value="RES-001", key="tab4_resume_id")
            search_text = st.text_area(
                "Resume Content",
                height=150,
                key="tab4_search_text_resume",
                value="John Doe - Senior Software Engineer with 7 years experience. Skills: Python, Java, React, AWS"
            )
    
    with col2:
        top_k = st.slider("Top K Results", min_value=1, max_value=10, value=5, key="tab4_top_k")
    
    st.divider()
    
    if st.button("🔎 Search", use_container_width=True):
        with st.spinner("Searching..."):
            try:
                if search_type == "Find Resumes for Job":
                    response = requests.post(
                        f"{st.session_state.api_url}/api/v1/match/job-to-resumes",
                        json={
                            "job_id": job_id_tab4,
                            "job_text": search_text,
                            "top_k": top_k
                        },
                        timeout=30
                    )
                else:
                    response = requests.post(
                        f"{st.session_state.api_url}/api/v1/match/resume-to-jobs",
                        json={
                            "resume_id": resume_id_tab4,
                            "resume_text": search_text,
                            "top_k": top_k
                        },
                        timeout=30
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success(f"✅ Found {result.get('matches_found', 0)} matches!")
                    
                    # Display matches
                    matches = result.get("matches", [])
                    if matches:
                        for i, match in enumerate(matches, 1):
                            with st.expander(
                                f"Match {i}: {match.get('metadata', {}).get('job_title' if search_type == 'Find Resumes for Job' else 'candidate_name', 'N/A')} "
                                f"(Score: {match.get('score', 0):.2%})"
                            ):
                                col1, col2 = st.columns([1, 2])
                                with col1:
                                    st.metric("Similarity Score", f"{match.get('score', 0):.2%}")
                                with col2:
                                    st.json(match.get("metadata", {}))
                                st.write("**Preview:**")
                                st.code(match.get("preview", "N/A")[:300])
                    else:
                        st.info("No matches found")
                    
                else:
                    st.error(f"API error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ==================== Footer ====================
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 Show History", use_container_width=True):
        if st.session_state.analysis_history:
            st.write("### Analysis History")
            hist_df = pd.DataFrame(st.session_state.analysis_history)
            st.dataframe(hist_df, use_container_width=True)
        else:
            st.info("No analysis history yet")

with col2:
    if st.button("🗑️ Clear Database", use_container_width=True):
        confirm = st.checkbox("I understand this will clear all data", key="clear_confirm")
        if confirm:
            try:
                response = requests.get(f"{st.session_state.api_url}/api/v1/admin/clear-db")
                if response.status_code == 200:
                    st.success("Database cleared!")
                else:
                    st.error("Failed to clear database")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with col3:
    if st.button("💾 Export Database", use_container_width=True):
        try:
            response = requests.get(f"{st.session_state.api_url}/api/v1/admin/export")
            if response.status_code == 200:
                st.success("Database exported!")
                st.json(response.json())
            else:
                st.error("Failed to export database")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("Made with ❤️ using CrewAI | v0.1.0")
