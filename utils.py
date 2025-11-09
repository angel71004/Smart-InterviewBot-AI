"""
Utility functions for Resume Analysis and Interview Question Generation
"""

import re
import PyPDF2
import pandas as pd
from docx import Document
from io import BytesIO
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load spaCy model (will be initialized in app)
nlp = None

# Common IT/Technical Skills Vocabulary
TECH_SKILLS = [
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'kotlin', 'swift',
    'php', 'ruby', 'scala', 'perl', 'r', 'matlab', 'sql', 'html', 'css', 'xml', 'json',
    
    # Frameworks & Libraries
    'react', 'angular', 'vue', 'django', 'flask', 'spring', 'node.js', 'express', 'fastapi',
    'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'scikit-learn', 'bootstrap', 'jquery',
    
    # Databases
    'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra', 'elasticsearch',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
    'ci/cd', 'terraform', 'ansible', 'linux', 'bash', 'shell scripting',
    
    # Tools & Technologies
    'git', 'jira', 'confluence', 'agile', 'scrum', 'kanban', 'rest api', 'graphql', 'microservices',
    'machine learning', 'deep learning', 'ai', 'data science', 'big data', 'hadoop', 'spark',
    
    # Web Technologies
    'html5', 'css3', 'sass', 'less', 'webpack', 'npm', 'yarn', 'redux', 'vuex',
    
    # Mobile
    'android', 'ios', 'react native', 'flutter', 'xamarin',
    
    # Other
    'oop', 'design patterns', 'tdd', 'unit testing', 'integration testing', 'api development',
    'software architecture', 'system design', 'algorithms', 'data structures'
]

# Soft Skills
SOFT_SKILLS = [
    'communication', 'leadership', 'teamwork', 'problem solving', 'time management',
    'project management', 'critical thinking', 'adaptability', 'creativity', 'collaboration'
]


def init_spacy_model():
    """Initialize spaCy model for NLP processing"""
    global nlp
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Warning: spaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
        nlp = None


def extract_text_from_pdf(file) -> str:
    """
    Extract text from PDF file
    
    Args:
        file: Uploaded file object from Streamlit
        
    Returns:
        Extracted text as string
    """
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_docx(file) -> str:
    """
    Extract text from DOCX file
    
    Args:
        file: Uploaded file object from Streamlit
        
    Returns:
        Extracted text as string
    """
    try:
        doc = Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")


def extract_skills_simple(text: str) -> list:
    """
    Extract skills from resume text using keyword matching and NLP
    
    Args:
        text: Resume text
        
    Returns:
        List of extracted skills
    """
    if not text:
        return []
    
    text_lower = text.lower()
    found_skills = []
    
    # Check for technical skills
    for skill in TECH_SKILLS:
        # Match whole words only
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower, re.IGNORECASE):
            found_skills.append(skill.title())
    
    # Use spaCy for additional skill extraction if available
    if nlp:
        try:
            doc = nlp(text)
            # Extract nouns and proper nouns that might be skills
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                    token_lower = token.text.lower()
                    if token_lower in TECH_SKILLS and token.text.title() not in found_skills:
                        found_skills.append(token.text.title())
        except:
            pass
    
    # Remove duplicates and return
    return sorted(list(set(found_skills)))

def load_job_roles(path):
    try:
        df = pd.read_csv(path, on_bad_lines='skip', engine='python', skip_blank_lines=True)
        expected_cols = ['Job_Role', 'Key_Skills']
        df = df[[col for col in df.columns if col in expected_cols]]
        return df.dropna(subset=['Job_Role', 'Key_Skills'])
    except Exception as e:
        print(f"❌ Error loading job roles: {e}")
        return pd.DataFrame(columns=['Job_Role', 'Key_Skills'])



def load_questions(path):
    try:
        df = pd.read_csv(path, on_bad_lines='skip', engine='python', skip_blank_lines=True)
        expected_cols = ['Job_Role', 'Question_Type', 'Question', 'Difficulty']
        df = df[[col for col in df.columns if col in expected_cols]]
        if 'Difficulty' not in df.columns:
            df['Difficulty'] = 'Medium'
        return df.dropna(subset=['Job_Role', 'Question_Type', 'Question'])
    except Exception as e:
        print(f"❌ Error loading questions: {e}")
        return pd.DataFrame(columns=['Job_Role', 'Question_Type', 'Question', 'Difficulty'])



def match_role_skills(role: str, resume_skills: list, job_roles_df: pd.DataFrame) -> dict:
    """
    Match resume skills with job role requirements
    
    Args:
        role: Selected job role
        resume_skills: List of skills extracted from resume
        job_roles_df: DataFrame containing job roles and required skills
        
    Returns:
        Dictionary with matched skills, missing skills, and match score
    """
    if job_roles_df.empty or role not in job_roles_df['Job_Role'].values:
        return {
            'matched_skills': [],
            'missing_skills': [],
            'match_score': 0
        }
    
    # Get required skills for the role
    role_row = job_roles_df[job_roles_df['Job_Role'] == role].iloc[0]
    required_skills_str = str(role_row['Key_Skills']).lower()
    
    # Parse required skills (assuming comma-separated)
    required_skills = [s.strip() for s in required_skills_str.split(',')]
    
    # Normalize resume skills for comparison
    resume_skills_lower = [s.lower() for s in resume_skills]
    
    # Find matched and missing skills
    matched_skills = []
    missing_skills = []
    
    for req_skill in required_skills:
        matched = False
        for res_skill in resume_skills_lower:
            # Check for partial matches
            if req_skill in res_skill or res_skill in req_skill:
                matched_skills.append(req_skill.title())
                matched = True
                break
        if not matched:
            missing_skills.append(req_skill.title())
    
    # Calculate match score
    if len(required_skills) > 0:
        match_score = (len(matched_skills) / len(required_skills)) * 100
    else:
        match_score = 0
    
    return {
        'matched_skills': sorted(list(set(matched_skills))),
        'missing_skills': sorted(list(set(missing_skills))),
        'match_score': round(match_score, 2)
    }


def get_questions_for_role(role: str, question_type: str, questions_df: pd.DataFrame) -> list:
    """
    Get questions for a specific role and type
    
    Args:
        role: Job role
        question_type: Type of question (Technical, Behavioral, Scenario-based)
        questions_df: DataFrame containing questions
        
    Returns:
        List of questions
    """
    if questions_df.empty:
        return []
    
    filtered = questions_df[
        (questions_df['Job_Role'] == role) & 
        (questions_df['Question_Type'] == question_type)
    ]
    return filtered['Question'].tolist()


def rank_questions_by_similarity(resume_text: str, questions: list, top_n: int = 10) -> list:
    """
    Rank questions by similarity to resume text using TF-IDF
    
    Args:
        resume_text: Resume text
        questions: List of questions
        top_n: Number of top questions to return
        
    Returns:
        Ranked list of questions
    """
    if not questions or not resume_text:
        return questions[:top_n] if questions else []
    
    try:
        # Combine resume text with questions
        documents = [resume_text] + questions
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity between resume and questions
        resume_vector = tfidf_matrix[0:1]
        question_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(resume_vector, question_vectors)[0]
        
        # Get indices of top similar questions
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        # Return ranked questions
        ranked_questions = [questions[i] for i in top_indices]
        return ranked_questions
    except Exception as e:
        print(f"Error in ranking questions: {str(e)}")
        return questions[:top_n]


def calculate_difficulty_score(question: str) -> str:
    """
    Simple heuristic to determine question difficulty
    
    Args:
        question: Question text
        
    Returns:
        Difficulty level: Easy, Medium, or Hard
    """
    question_lower = question.lower()
    
    # Hard keywords
    hard_keywords = ['design', 'architecture', 'scalability', 'distributed', 'algorithm', 
                     'complexity', 'optimization', 'system design', 'concurrency']
    
    # Medium keywords
    medium_keywords = ['explain', 'difference', 'how', 'what', 'describe', 'implement']
    
    # Easy keywords
    easy_keywords = ['define', 'list', 'name', 'what is', 'basic']
    
    hard_count = sum(1 for kw in hard_keywords if kw in question_lower)
    medium_count = sum(1 for kw in medium_keywords if kw in question_lower)
    easy_count = sum(1 for kw in easy_keywords if kw in question_lower)
    
    if hard_count >= 2 or len(question.split()) > 30:
        return "Hard"
    elif medium_count > easy_count or len(question.split()) > 15:
        return "Medium"
    else:
        return "Easy"

