# 🚀 Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### Step 3: Verify Setup
```bash
python verify_setup.py
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

## Usage (3 steps)

1. **Upload Resume**: Go to "Resume Upload" tab → Upload PDF/DOCX file
2. **Select Role**: Go to "Analysis & Questions" tab → Choose job role
3. **Get Questions**: View personalized questions → Download as CSV

## Features Checklist

- ✅ Resume upload (PDF/DOCX)
- ✅ Skill extraction
- ✅ Job role matching
- ✅ Match score calculation
- ✅ Personalized questions
- ✅ Question ranking
- ✅ CSV download
- ✅ Statistics dashboard

## Troubleshooting

**Problem**: spaCy model not found
**Solution**: `python -m spacy download en_core_web_sm`

**Problem**: No skills detected
**Solution**: Ensure resume contains technical keywords (Python, Java, SQL, etc.)

**Problem**: Questions not showing
**Solution**: Check that job_roles.csv and interview_questions.csv exist

## Next Steps

1. Add your own resume to test
2. Customize job roles in `job_roles.csv`
3. Add more questions in `interview_questions.csv`
4. Deploy to Streamlit Cloud for sharing

---

**Happy Interview Preparation! 🎯**

