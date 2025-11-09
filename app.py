"""
AI-Powered Interview Question Generator with Resume Analysis
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import os
from utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_skills_simple,
    load_job_roles,
    load_questions,
    match_role_skills,
    get_questions_for_role,
    rank_questions_by_similarity,
    calculate_difficulty_score,
    init_spacy_model,
    TECH_SKILLS
)
import io
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Interview Question Generator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        padding: 0.5rem;
    }
    .skill-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        background-color: #e3f2fd;
        border-radius: 15px;
        font-size: 0.9rem;
    }
    .match-score {
        font-size: 2rem;
        font-weight: bold;
        color: #4caf50;
    }
    .question-card {
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        background-color: #f5f5f5;
        border-radius: 5px;
    }
    .difficulty-easy {
        color: #4caf50;
        font-weight: bold;
    }
    .difficulty-medium {
        color: #ff9800;
        font-weight: bold;
    }
    .difficulty-hard {
        color: #f44336;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'extracted_skills' not in st.session_state:
    st.session_state.extracted_skills = []
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None

# Initialize spaCy model
@st.cache_resource
def load_nlp_model():
    """Load spaCy model with caching"""
    init_spacy_model()
    return True

load_nlp_model()

# Main header
st.markdown('<h1 class="main-header">💼 AI Interview Question Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload your resume, select a job role, and get personalized interview questions!</p>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("📋 Navigation")
st.sidebar.markdown("---")

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOB_ROLES_PATH = os.path.join(BASE_DIR, "job_roles.csv")
QUESTIONS_PATH = os.path.join(BASE_DIR, "interview_questions.csv")

# Load data
@st.cache_data
def load_data():
    """Load job roles and questions data"""
    try:
        job_roles_df = load_job_roles(JOB_ROLES_PATH)
        questions_df = load_questions(QUESTIONS_PATH)
        return job_roles_df, questions_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(), pd.DataFrame()

job_roles_df, questions_df = load_data()

# Main content area
tab1, tab2, tab3 = st.tabs(["📄 Resume Upload", "🔍 Analysis & Questions", "📊 Statistics"])

with tab1:
    st.header("📄 Upload Your Resume")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Choose a resume file (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Upload your resume in PDF or DOCX format"
    )
    
    if uploaded_file is not None:
        # Display file details
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.write("**File Details:**")
        st.json(file_details)
        
        # Extract text based on file type
        try:
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                st.error("Unsupported file type. Please upload a PDF or DOCX file.")
                resume_text = ""
            
            if resume_text:
                st.session_state.resume_text = resume_text
                
                # Extract skills
                with st.spinner("Extracting skills from resume..."):
                    extracted_skills = extract_skills_simple(resume_text)
                    st.session_state.extracted_skills = extracted_skills
                
                st.success("✅ Resume processed successfully!")
                
                # Display extracted text preview
                with st.expander("📝 View Extracted Resume Text", expanded=False):
                    st.text_area("Resume Text", resume_text, height=200, disabled=True)
                
                # Display extracted skills
                if extracted_skills:
                    st.subheader("🎯 Extracted Skills")
                    skills_html = " ".join([f'<span class="skill-badge">{skill}</span>' for skill in extracted_skills])
                    st.markdown(skills_html, unsafe_allow_html=True)
                    st.write(f"**Total Skills Found:** {len(extracted_skills)}")
                else:
                    st.warning("⚠️ No skills detected in the resume. Make sure your resume contains technical skills and keywords.")
            else:
                st.error("Failed to extract text from the resume. Please try another file.")
        except Exception as e:
            st.error(f"Error processing resume: {str(e)}")
    else:
        st.info("👆 Please upload a resume file to get started.")

with tab2:
    st.header("🔍 Analysis & Interview Questions")
    st.markdown("---")
    
    if not st.session_state.resume_text:
        st.warning("⚠️ Please upload a resume in the 'Resume Upload' tab first.")
    else:
        # Job role selection
        st.subheader("🎯 Select Job Role")
        
        if not job_roles_df.empty:
            job_roles = job_roles_df['Job_Role'].unique().tolist()
            selected_role = st.selectbox(
                "Choose a job role:",
                options=job_roles,
                help="Select the job role you're applying for"
            )
            st.session_state.selected_role = selected_role
            
            if selected_role:
                # Skill matching
                st.markdown("---")
                st.subheader("🔗 Skill Matching Analysis")
                
                match_results = match_role_skills(
                    selected_role,
                    st.session_state.extracted_skills,
                    job_roles_df
                )
                
                # Display match score
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Match Score", f"{match_results['match_score']:.1f}%")
                with col2:
                    st.metric("Matched Skills", len(match_results['matched_skills']))
                with col3:
                    st.metric("Missing Skills", len(match_results['missing_skills']))
                
                # Progress bar for match score
                st.progress(match_results['match_score'] / 100)
                
                # Display matched skills
                if match_results['matched_skills']:
                    st.write("**✅ Matched Skills:**")
                    matched_skills_html = " ".join([
                        f'<span class="skill-badge" style="background-color: #c8e6c9;">{skill}</span>' 
                        for skill in match_results['matched_skills']
                    ])
                    st.markdown(matched_skills_html, unsafe_allow_html=True)
                
                # Display missing skills
                if match_results['missing_skills']:
                    st.write("**⚠️ Missing Skills (Recommended to add):**")
                    missing_skills_html = " ".join([
                        f'<span class="skill-badge" style="background-color: #ffcdd2;">{skill}</span>' 
                        for skill in match_results['missing_skills']
                    ])
                    st.markdown(missing_skills_html, unsafe_allow_html=True)
                
                # Generate and display questions
                st.markdown("---")
                st.subheader("❓ Personalized Interview Questions")
                
                if not questions_df.empty:
                    # Get questions for each category
                    technical_questions = get_questions_for_role(selected_role, "Technical", questions_df)
                    behavioral_questions = get_questions_for_role(selected_role, "Behavioral", questions_df)
                    scenario_questions = get_questions_for_role(selected_role, "Scenario-based", questions_df)
                    
                    # Rank questions by similarity to resume
                    if st.session_state.resume_text:
                        if technical_questions:
                            technical_questions = rank_questions_by_similarity(
                                st.session_state.resume_text,
                                technical_questions,
                                top_n=10
                            )
                        if behavioral_questions:
                            behavioral_questions = rank_questions_by_similarity(
                                st.session_state.resume_text,
                                behavioral_questions,
                                top_n=10
                            )
                        if scenario_questions:
                            scenario_questions = rank_questions_by_similarity(
                                st.session_state.resume_text,
                                scenario_questions,
                                top_n=10
                            )
                    
                    # Display questions by category
                    question_categories = {
                        "🛠️ Technical Questions": technical_questions,
                        "💬 Behavioral Questions": behavioral_questions,
                        "🎯 Scenario-based Questions": scenario_questions
                    }
                    
                    for category_name, questions in question_categories.items():
                        if questions:
                            with st.expander(category_name, expanded=True):
                                for idx, question in enumerate(questions, 1):
                                    difficulty = calculate_difficulty_score(question)
                                    difficulty_class = f"difficulty-{difficulty.lower()}"
                                    
                                    st.markdown(f"""
                                    <div class="question-card">
                                        <strong>Q{idx}:</strong> {question}<br>
                                        <span class="{difficulty_class}">Difficulty: {difficulty}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.info(f"No {category_name.lower()} available for this role.")
                    
                    # Download questions as CSV
                    st.markdown("---")
                    st.subheader("💾 Download Questions")
                    
                    # Prepare download data
                    all_questions_data = []
                    for category_name, questions in question_categories.items():
                        for question in questions:
                            difficulty = calculate_difficulty_score(question)
                            all_questions_data.append({
                                "Category": category_name.replace("🛠️ ", "").replace("💬 ", "").replace("🎯 ", ""),
                                "Question": question,
                                "Difficulty": difficulty,
                                "Job Role": selected_role
                            })
                    
                    if all_questions_data:
                        download_df = pd.DataFrame(all_questions_data)
                        
                        # Convert to CSV
                        csv_buffer = io.StringIO()
                        download_df.to_csv(csv_buffer, index=False)
                        csv_data = csv_buffer.getvalue()
                        
                        st.download_button(
                            label="📥 Download Questions as CSV",
                            data=csv_data,
                            file_name=f"interview_questions_{selected_role}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            help="Download all generated questions as a CSV file"
                        )
                else:
                    st.error("No questions available. Please check the questions CSV file.")
        else:
            st.error("No job roles available. Please check the job_roles.csv file.")

with tab3:
    st.header("📊 Statistics & Insights")
    st.markdown("---")
    
    if not st.session_state.resume_text:
        st.warning("⚠️ Please upload a resume to see statistics.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Resume Statistics")
            st.metric("Total Characters", len(st.session_state.resume_text))
            st.metric("Total Words", len(st.session_state.resume_text.split()))
            st.metric("Total Skills Detected", len(st.session_state.extracted_skills))
            
            # Skills distribution
            if st.session_state.extracted_skills:
                st.write("**Skills Breakdown:**")
                skills_df = pd.DataFrame({
                    "Skill": st.session_state.extracted_skills,
                    "Category": ["Technical"] * len(st.session_state.extracted_skills)
                })
                st.dataframe(skills_df, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Role Match Statistics")
            if st.session_state.selected_role and not job_roles_df.empty:
                match_results = match_role_skills(
                    st.session_state.selected_role,
                    st.session_state.extracted_skills,
                    job_roles_df
                )
                
                # Create match visualization
                match_data = {
                    "Metric": ["Match Score", "Matched Skills", "Missing Skills"],
                    "Value": [
                        match_results['match_score'],
                        len(match_results['matched_skills']),
                        len(match_results['missing_skills'])
                    ]
                }
                match_df = pd.DataFrame(match_data)
                st.bar_chart(match_df.set_index("Metric"))
                
                # Recommendations
                st.write("**💡 Recommendations:**")
                if match_results['match_score'] < 50:
                    st.warning("Your resume has a low match score. Consider adding more relevant skills.")
                elif match_results['match_score'] < 75:
                    st.info("Your resume has a moderate match score. Adding a few more skills could improve it.")
                else:
                    st.success("Your resume has a high match score! You're well-aligned with the role requirements.")
            else:
                st.info("Select a job role to see match statistics.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>💼 AI Interview Question Generator | Powered by Streamlit & NLP</p>
        <p>Upload your resume, get personalized interview questions, and ace your next interview!</p>
    </div>
""", unsafe_allow_html=True)

